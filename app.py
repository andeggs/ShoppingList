import os
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
    
    prompt = f"""I have the following meals planned: {meal_list}

Please provide a comprehensive shopping list of all ingredients needed to make these meals. 
Format the response as a clear, organized list of ingredients with quantities where appropriate.
Group similar items together (e.g., all vegetables, all proteins, etc.)."""
    
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        ingredients = response.text if response.text else "Unable to generate shopping list."
        return jsonify({'ingredients': ingredients}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate shopping list: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
