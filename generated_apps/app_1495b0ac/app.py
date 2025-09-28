from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'tom_cafe.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/menu', methods=['GET'])
def get_menu():
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM menu_items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in menu_items])

@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    conn = get_db_connection()
    promotions = conn.execute('SELECT * FROM promotions').fetchall()
    conn.close()
    return jsonify([dict(promotion) for promotion in promotions])

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    user_id = data['user_id']
    table_number = data['table_number']
    reservation_time = data['reservation_time']
    status = data['status']

    conn = get_db_connection()
    conn.execute('INSERT INTO reservations (user_id, table_number, reservation_time, status) VALUES (?, ?, ?, ?)',
                 (user_id, table_number, reservation_time, status))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Reservation created successfully!'}), 201

@app.route('/api/payments', methods=['POST'])
def process_payment():
    data = request.json
    # Here you would typically process the payment with a payment gateway
    # For demonstration purposes, we'll just return a success message
    return jsonify({'message': 'Payment processed successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
```

### คำอธิบาย:
1. **Flask**: ใช้สำหรับสร้าง API endpoints
2. **SQLite**: เชื่อมต่อกับฐานข้อมูล SQLite
3. **CORS**: ใช้ `flask_cors` เพื่อให้รองรับ CORS
4. **Endpoints**: สร้าง API endpoints ตามที่ระบุไว้ในคำถาม

### หมายเหตุ:
- คุณต้องสร้างฐานข้อมูล SQLite และตารางตาม schema ที่ให้ไว้ก่อนที่จะรันโค้ดนี้
- คุณสามารถใช้ SQLite command line หรือ SQLite GUI tools เพื่อสร้างฐานข้อมูลและตารางได้
- อย่าลืมติดตั้ง Flask และ Flask-CORS ด้วยคำสั่ง `pip install Flask Flask-CORS` ก่อนรันโ