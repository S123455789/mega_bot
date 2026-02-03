import sqlite3

def init():
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id TEXT
    )""")

    db.commit()
    db.close()

def add(user_id):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    db.commit()
    db.close()

def all_users():
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT user_id FROM users")
    data = c.fetchall()

    return [i[0] for i in data]