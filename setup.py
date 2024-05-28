import sqlite3

def create_users_table():
    conn = sqlite3.connect('promos.db')
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS promos')
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (login TEXT, name TEXT,password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS promos (id INT, promo TEXT)')
    cursor.execute("INSERT INTO promos (id, promo) VALUES (1, 'TEST_PROMO')")

    conn.commit()
    conn.close()





create_users_table()
