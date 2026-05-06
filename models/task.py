from datetime import datetime

class Task():
    def __init__(self, id, user_id, title, description, status, created_at):
        self.id = id
        self.user_ide = user_id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%d/%m/%Y %H:%M")