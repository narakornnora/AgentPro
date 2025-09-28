import sqlite3
from datetime import datetime

# สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# สร้างตาราง users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT
)
''')

# สร้างตาราง reservations
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    reservation_time DATETIME NOT NULL,
    number_of_people INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# สร้างตาราง promotions
cursor.execute('''
CREATE TABLE IF NOT EXISTS promotions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL
)
''')

# สร้างตาราง restaurant_info
cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurant_info (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    opening_hours TEXT NOT NULL
)
''')

# เพิ่มข้อมูลตัวอย่างในตาราง users
cursor.execute('''
INSERT INTO users (username, email, phone_number) VALUES
('john_doe', 'john@example.com', '1234567890'),
('jane_smith', 'jane@example.com', '0987654321')
''')

# เพิ่มข้อมูลตัวอย่างในตาราง reservations
cursor.execute('''
INSERT INTO reservations (user_id, reservation_time, number_of_people, status) VALUES
(1, ?, 2, 'confirmed'),
(2, ?, 4, 'pending')
''', (datetime.now(), datetime.now()))

# เพิ่มข้อมูลตัวอย่างในตาราง promotions
cursor.execute('''
INSERT INTO promotions (title, description, start_date, end_date) VALUES
('Happy Hour', '50% off on drinks', ?, ?)
''', (datetime.now(), datetime.now()))

# เพิ่มข้อมูลตัวอย่างในตาราง restaurant_info
cursor.execute('''
INSERT INTO restaurant_info (address, opening_hours) VALUES
('123 Food St, Flavor Town', '10:00 AM - 10:00 PM')
''')

# บันทึกการเปลี่ยนแปลงและปิดการเชื่อมต่อ
conn.commit()
conn.close()

print("Database and tables created, sample data inserted successfully.")