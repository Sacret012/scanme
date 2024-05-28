import sqlite3

def register_user(login, name, password):
    try:
        conn = sqlite3.connect('promos.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        if cursor.fetchone() is not None:
            conn.close()
            return False
    
        cursor.execute('INSERT INTO users (login, name, password) VALUES (?, ?, ?)', (login, name, password))
    
        conn.commit()
        conn.close()
    
        return True
    except Exception as e:
        return False

def get_login(login, password):
    try:
        conn = sqlite3.connect('promos.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
        user = cursor.fetchone()
    
        conn.close()
    
        if user is not None:
            return True
        else:
            return False
    except Exception as e:
        return False
    
def get_user_nickname(login):
    conn = sqlite3.connect('promos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE login = '" + login +"'")
    user = cursor.fetchone()
    
    conn.close()
    
    if user is not None:
        return user[0]  
    else:
        return ""


