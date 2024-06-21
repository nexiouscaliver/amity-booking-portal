import sqlite3

# Connect to the database
conn = sqlite3.connect('testbooking.db')
cursor = conn.cursor()

# Create a table for venue halls
cursor.execute('''
        CREATE TABLE IF NOT EXISTS halls (
        hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        hall_id INTEGER,
        date TEXT,
        booked BOOLEAN DEFAULT 0
    )
''')
conn.commit()
conn.close()


venue = [0,"Auditorium","Seminar","A2","CRC"]
# 1 > Audi
# 2 > seminar
# 3 > A2
# 4 > crc
# DD-MM-YY
#(1, 'audi', 1, '20-06-2024', 1)
#bid,name,hid,date,booked
#fucntion to check avaibility
def check_hall(venue_id,date):
    conn = sqlite3.connect('testbooking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM booking WHERE hall_id = ? AND date = ?', (venue_id,date))
    venue = cursor.fetchone()
    conn.commit()
    conn.close()
    if venue:
        if not venue[4]:
            print(f"Venue hall '{venue[1]}' is not verified")
            return "Not Verified"
        else:
            print(f"Venue hall '{venue[1]}' is already booked.")
            return False
    else:
        print("No request given.")
        return True
    # return (venue)

#send request
def book_venue_hall_request(name,venue_id,date):
    conn = sqlite3.connect('testbooking.db')
    cursor = conn.cursor() 
    sql = f'insert into booking (name,hall_id,date,booked) values ("{name}","{venue_id}","{date}",0);'
    cursor.execute(sql)
    conn.commit()
    print(f"Venue hall '{name}' has been requested successfully!")
    conn.commit()
    conn.close()


# Function to book a venue hall
def book_venue_hall_confirm(name,venue_id,date):
    conn = sqlite3.connect('testbooking.db')
    cursor = conn.cursor()
    # cursor.execute('SELECT * FROM booking WHERE hall_id = ?', (venue_id,))
    # venue = cursor.fetchone()

    # if venue:
    #     if not venue[3]:  # Check if the venue is already booked
    #         cursor.execute('UPDATE halls SET booked = 1 WHERE id = ?', (venue_id,))
    #         conn.commit()
    #         print(f"Venue hall '{venue[1]}' has been booked successfully!")
    #     else:
    #         print(f"Venue hall '{venue[1]}' is already booked.")
    # else:
    #     print("Invalid venue hall ID.")
    sql = f'update booking set booked = 1 where name="{name}" and hall_id={venue_id} and date={date};'
    print(sql)
    cursor.execute(sql)
    conn.commit()
    print(f"Venue hall '{name}' has been booked successfully!")
    conn.commit()
    conn.close()

# Function to display all available venue halls
def display_venue_halls():
    cursor.execute('SELECT * FROM halls')
    venue_halls = cursor.fetchall()

    if venue_halls:
        print("Available venue halls:")
        for venue in venue_halls:
            print(f"ID: {venue[0]}, Name: {venue[1]}, Capacity: {venue[2]}, Booked: {'Yes' if venue[3] else 'No'}")
    else:
        print("No venue halls found.")

# Main program loop
# while True:
#     print("\n1. Book a venue hall")
#     print("2. Display available venue halls")
#     print("3. Exit")

#     choice = input("Enter your choice (1-3): ")

#     if choice == '1':
#         venue_id = input("Enter the ID of the venue hall you want to book: ")
#         book_venue_hall(venue_id)
#     elif choice == '2':
#         display_venue_halls()
#     elif choice == '3':
#         break
#     else:
#         print("Invalid choice. Please try again.")

# Close the database connection
# conn.close()