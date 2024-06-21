import sqlite3

# Connect to the database
conn = sqlite3.connect('booking.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS halls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        booked BOOLEAN DEFAULT 0
    )
''')

cursor.execute("""insert into halls (name) values ('Audi'),('seminar'),('A2'),('crc'); """)