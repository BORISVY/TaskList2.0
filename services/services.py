from data.db import connect
from contextlib import contextmanager
from utils.security import hash_password, verify_password

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
    
class UserTaskService:
    def new_user(self, username, email, password):
        hashed_password = hash_password(password)
        with connection() as cursor:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            return cursor.rowcount
        
    def login(self, username, password):
        with connection() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if not user:
                return None

            stored_hash = user[3]

            if not verify_password(password, stored_hash):
                return None
            return user
            
    def edit_username(self, user_id, new_username):
        with connection() as cursor:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            return cursor.rowcount
    
    def delete_user(self, user_id):
        with connection() as cursor:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount

    def get_user(self, user_id):
        with connection() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            return cursor.fetchone()

    def new_task(self, user_id, title, description):
        with connection() as cursor:
            cursor.execute("INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                           (user_id, title, description))
            return cursor.rowcount
    
    def complete_task(self, task_id):
        with connection() as cursor:
            cursor.execute("UPDATE tasks SET status = 1 WHERE id = ?", (task_id,))
            return cursor.rowcount

    def reopen_task(self, task_id):
        with connection() as cursor:
            cursor.execute("UPDATE tasks SET status = 0 WHERE id = ?", (task_id,))
            return cursor.rowcount

    def get_tasks_by_user(self, user_id):
        with connection() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))   
            return cursor.fetchall()

    def get_task_by_id(self, task_id):
        with connection() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()     
        
    def get_all_tasks(self):
        with connection() as cursor:
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()
        
    def edit_title_task(self, task_id, new_title):
        with connection() as cursor:
            cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
            return cursor.rowcount
        
    def edit_desc_task(self, task_id, new_description):
        with connection() as cursor:
            cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
            return cursor.rowcount

    def delete_task(self, task_id):
        with connection() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))