import os
import json
from flask import Flask, render_template, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from google import genai

app = Flask(__name__)

gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meals', methods=['GET'])
def get_meals():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, name, created_at FROM meals ORDER BY created_at DESC')
    meals = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify({'meals': meals})

@app.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    meal_name = data.get('name', '').strip()
    
    if not meal_name:
        return jsonify({'error': 'Meal name cannot be empty'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO meals (name) VALUES (%s) RETURNING id, name, created_at', (meal_name,))
    new_meal = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'meal': new_meal}), 201

@app.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM meals WHERE id = %s', (meal_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'success': True}), 200

@app.route('/shopping-list', methods=['POST'])
def create_shopping_list():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT name FROM meals ORDER BY created_at DESC')
    meals = cur.fetchall()
    cur.close()
    conn.close()
    
    if not meals:
        return jsonify({'error': 'No meals found. Please add some meals first.'}), 400
    
    meal_names = [meal['name'] for meal in meals]
    meal_list = ', '.join(meal_names)
    
    prompt = f"""**Generate a consolidated shopping list for the following meals in well-formatted JSON:**

{meal_list}

**The JSON object must contain an array of ingredients.** Each ingredient object must include:
1.  **"name"**: The name of the ingredient.
2.  **"is_gf_alternative_available"**: A boolean value (true/false) indicating if a Gluten-Free alternative exists.
3.  **"is_lf_alternative_available"**: A boolean value (true/false) indicating if a Lactose-Free alternative exists.
4.  **"meals"**: An array listing the meals this ingredient is used in.

**Example JSON structure:**
{{
  "shopping_list": [
    {{
      "name": "Spaghetti",
      "is_gf_alternative_available": true,
      "is_lf_alternative_available": false,
      "meals": ["spaghetti bolognese"]
    }},
  ]
}}
**Important:** Return ONLY the JSON object, no markdown code blocks, no additional text."""
    
    response = None
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        if not response.text:
            return jsonify({'error': 'Unable to generate shopping list.'}), 500
        
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        shopping_data = json.loads(response_text)
        return jsonify(shopping_data), 200
        
    except json.JSONDecodeError as e:
        error_msg = f'Failed to parse shopping list: {str(e)}'
        if response and response.text:
            return jsonify({'error': error_msg, 'raw_response': response.text}), 500
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to generate shopping list: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
