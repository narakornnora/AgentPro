import sqlite3

# สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# ฟังก์ชันสำหรับสร้างตารางตาม schema ที่กำหนด
def create_tables():
    # สร้างตาราง users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # สร้างตาราง menu_items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT
        )
    ''')

    # สร้างตาราง promotions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promotions (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            details TEXT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL
        )
    ''')

    # สร้างตาราง reservations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            table_number INTEGER NOT NULL,
            reservation_time DATETIME NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

# ฟังก์ชันสำหรับเพิ่มข้อมูลตัวอย่าง
def insert_sample_data():
    # เพิ่มข้อมูลตัวอย่างในตาราง users
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                   ('john_doe', 'john@example.com', 'securepassword'))
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                   ('jane_doe', 'jane@example.com', 'securepassword'))

    # เพิ่มข้อมูลตัวอย่างในตาราง menu_items
    cursor.execute("INSERT INTO menu_items (name, description, price, category) VALUES (?, ?, ?, ?)", 
                   ('Pasta', 'Delicious pasta with tomato sauce', 8.99, 'Main Course'))
    cursor.execute("INSERT INTO menu_items (name, description, price, category) VALUES (?, ?, ?, ?)", 
                   ('Caesar Salad', 'Fresh salad with Caesar dressing', 5.99, 'Salad'))

    # เพิ่มข้อมูลตัวอย่างในตาราง promotions
    cursor.execute("INSERT INTO promotions (title, details, start_date, end_date) VALUES (?, ?, ?, ?)", 
                   ('Happy Hour', 'Get 50% off on drinks', '2023-10-01', '2023-10-31'))

    # เพิ่มข้อมูลตัวอย่างในตาราง reservations
    cursor.execute("INSERT INTO reservations (user_id, table_number, reservation_time, status) VALUES (?, ?, ?, ?)", 
                   (1, 5, '2023-10-15 19:00:00', 'Confirmed'))

# เรียกใช้ฟังก์ชันเพื่อสร้างตารางและเพิ่มข้อมูลตัวอย่าง
create_tables()
insert_sample_data()

# บันทึกการเปลี่ยนแปลงและปิดการเชื่อมต่อ
conn.commit()
conn.close()