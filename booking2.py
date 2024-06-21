import sqlite3

conn = sqlite3.connect('test2.db')
cursor = conn.cursor()
venue = [0,"Auditorium","Seminar","A2","CRC"]
#init

def init():
    cursor.execute('CREATE TABLE IF NOT EXISTS booking (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, hall_id INTEGER, date TEXT, booked INTEGER);')
    conn.commit()