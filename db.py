import sqlite3

def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        table_number INTEGER,
        booking_time TEXT,
        booking_end_time TEXT
    )
    ''')
    conn.commit()
    conn.close()