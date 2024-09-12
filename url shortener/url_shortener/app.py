from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random

app = Flask(__name__)

DATABASE = 'db.sqlite3'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_table():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                long_url TEXT NOT NULL,
                short_code TEXT NOT NULL UNIQUE
            )
        ''')

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()

        with get_db() as conn:
            conn.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
        
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    with get_db() as conn:
        cur = conn.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
        result = cur.fetchone()

    if result:
        return redirect(result[0])
    else:
        return f"URL not found for the code: {short_code}", 404

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

import sqlite3

DATABASE = 'db.sqlite3'

def get_db():
    """Connect to the database and return the connection."""
    conn = sqlite3.connect(DATABASE)
    return conn

def create_table():
    """Create the URLs table if it doesn't exist."""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                long_url TEXT NOT NULL,
                short_code TEXT NOT NULL UNIQUE
            )
        ''')
    print("Database table created successfully.")

# Call create_table to ensure the table is created
if __name__ == '__main__':
    create_table()
