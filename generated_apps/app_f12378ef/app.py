from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('coffee_table_reservation.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if they don't exist
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                table_type TEXT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                number_of_people INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initialize the database
init_db()

# API Endpoints

@app.route('/api/users', methods=['GET'])
def get_users():
    with get_db_connection() as conn:
        users = conn.execute('SELECT * FROM users').fetchall()
        return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    new_user = request.json
    with get_db_connection() as conn:
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (new_user['username'], new_user['email'], new_user['password']))
        conn.commit()
    return jsonify(new_user), 201

@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    with get_db_connection() as conn:
        reservations = conn.execute('SELECT * FROM reservations').fetchall()
        return jsonify([dict(reservation) for reservation in reservations])

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    new_reservation = request.json
    with get_db_connection() as conn:
        conn.execute('INSERT INTO reservations (user_id, table_type, date, time, number_of_people) VALUES (?, ?, ?, ?, ?)',
                     (new_reservation['user_id'], new_reservation['table_type'], new_reservation['date'], new_reservation['time'], new_reservation['number_of_people']))
        conn.commit()
    return jsonify(new_reservation), 201

@app.route('/api/menu', methods=['GET'])
def get_menu():
    with get_db_connection() as conn:
        menu_items = conn.execute('SELECT * FROM menu_items').fetchall()
        return jsonify([dict(item) for item in menu_items])

if __name__ == '__main__':
    app.run(debug=True)