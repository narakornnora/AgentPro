from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'restaurant_booking.db'

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

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    new_reservation = request.json
    user_id = new_reservation['user_id']
    reservation_time = new_reservation['reservation_time']
    number_of_people = new_reservation['number_of_people']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO reservations (user_id, reservation_time, number_of_people) VALUES (?, ?, ?)',
                 (user_id, reservation_time, number_of_people))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    conn = get_db_connection()
    promotions = conn.execute('SELECT * FROM promotions').fetchall()
    conn.close()
    return jsonify([dict(promotion) for promotion in promotions])

@app.route('/api/restaurant_info', methods=['GET'])
def get_restaurant_info():
    conn = get_db_connection()
    restaurant_info = conn.execute('SELECT * FROM restaurant_info').fetchall()
    conn.close()
    return jsonify([dict(info) for info in restaurant_info])

if __name__ == '__main__':
    app.run(debug=True)
```

### คำอธิบาย
1. **Flask**: ใช้สำหรับสร้าง API endpoints
2. **CORS**: ใช้เพื่อให้สามารถเข้าถึง API จากโดเมนอื่นได้
3. **SQLite**: ใช้เป็นฐานข้อมูลสำหรับเก็บข้อมูลผู้ใช้ การจอง โปรโมชั่น และข้อมูลร้านอาหาร
4. **API Endpoints**: มีครบตามที่ระบุไว้ในคำถาม

### หมายเหตุ
- คุณต้องสร้างฐานข้อมูล SQLite และตารางตาม schema ที่ระบุไว้ก่อนที่จะรันโค้ดนี้
- คำสั่ง `app.run(debug=True)` จะทำให้แอปทำงานในโหมด debug ซึ่งเหมาะสำหรับการพัฒนา แต่ไม่ควรใช้ใน producti