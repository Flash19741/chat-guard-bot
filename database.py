import sqlite3
from datetime import datetime

DB_NAME = "chat_guard.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_seen TEXT
        )
    ''')
    conn.commit()
    conn.close()

def check_and_update_user(user_id: int, username: str, first_name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute("SELECT last_seen FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name, last_seen) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name, now)
        )
        conn.commit()
        conn.close()
        return "new"
    else:
        last_seen_time = datetime.fromisoformat(row[0])
        time_diff = (datetime.now() - last_seen_time).total_seconds()
        
        cursor.execute("UPDATE users SET last_seen = ? WHERE user_id = ?", (now, user_id))
        conn.commit()
        conn.close()
        
        if time_diff > 3600:
            return "returned"
        
        return "active"

init_db()