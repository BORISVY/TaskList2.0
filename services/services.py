from data.db import connect
from contextlib import contextmanager

@contextmanager
def connection():
    conn = connect()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

class Services():
    def new_user(self, username, email, password):
        with connection() as cursor:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            
    def edit_username(self, user_id, new_username):
        with connection() as cursor:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
    
    def delete_user(self, user_id):
        with connection() as cursor:
            cursor.execute("DEFELE FROM users WHERE id = ?", (user_id))