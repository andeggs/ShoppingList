import os
from flask import Flask, render_template, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('DROP TABLE IF EXISTS meals')
    cur.execute('''
        CREATE TABLE meals (
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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
