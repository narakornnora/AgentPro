import sqlite3

# สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# ฟังก์ชันสำหรับสร้างตาราง
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

    # สร้างตาราง reservations
    cursor.execute('''
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

    # สร้างตาราง menu_items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    # บันทึกการเปลี่ยนแปลง
    conn.commit()

# ฟังก์ชันสำหรับเพิ่มข้อมูลตัวอย่าง
def insert_sample_data():
    # เพิ่มข้อมูลในตาราง users
    cursor.execute('''
        INSERT INTO users (username, email, password) VALUES
        ('john_doe', 'john@example.com', 'password123'),
        ('jane_smith', 'jane@example.com', 'securepassword')
    ''')

    # เพิ่มข้อมูลในตาราง menu_items
    cursor.execute('''
        INSERT INTO menu_items (name, description, price, category) VALUES
        ('Spaghetti', 'Delicious spaghetti with tomato sauce', 8.99, 'Main Course'),
        ('Caesar Salad', 'Fresh romaine lettuce with Caesar dressing', 5.99, 'Salad'),
        ('Cheesecake', 'Creamy cheesecake with a graham cracker crust', 4.99, 'Dessert')
    ''')

    # เพิ่มข้อมูลในตาราง reservations
    cursor.execute('''
        INSERT INTO reservations (user_id, table_type, date, time, number_of_people) VALUES
        (1, 'Indoor', '2023-10-01', '18:30:00', 2),
        (2, 'Outdoor', '2023-10-02', '19:00:00', 4)
    ''')

    # บันทึกการเปลี่ยนแปลง
    conn.commit()

# สร้างตาราง
create_tables()

# เพิ่มข้อมูลตัวอย่าง
insert_sample_data()

# ปิดการเชื่อมต่อ
conn.close()