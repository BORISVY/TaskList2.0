import sqlite3
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(FOLDER, "secrets.db")

def connect():
    return sqlite3.connect(DB)

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL CHECK (email LIKE '%@%.%'),
            password BLOB NOT NULL)
                   ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            status BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)
                   ''')
    
    conn.commit()
    conn.close()

create_table()