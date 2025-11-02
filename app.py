import os
import random
from flask import Flask, render_template, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('DROP TABLE IF EXISTS messages')
    cur.execute('''
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    ''')
    
    messages = [
        "Have a wonderful day!",
        "You're doing amazing!",
        "Keep up the great work!",
        "Believe in yourself!",
        "Success is just around the corner!"
    ]
    
    for msg in messages:
        cur.execute('INSERT INTO messages (content) VALUES (%s)', (msg,))
    
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random-message')
def random_message():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT content FROM messages ORDER BY RANDOM() LIMIT 1')
    message = cur.fetchone()
    cur.close()
    conn.close()
    
    if message:
        return jsonify({'message': message['content']})
    else:
        return jsonify({'message': 'No messages found'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
