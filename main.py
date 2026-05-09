from srv.services import UserTaskService
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

service = UserTaskService()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    new_username: str

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TaskTitleUpdate(BaseModel):
    new_title: str

class TaskDescriptionUpdate(BaseModel):
    new_description: str

@app.post("/login")
def login(data: LoginRequest):
    user = service.login(data.username, data.password)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário ou senha inválidos")
    return {
        "message": "Login realizado com sucesso",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@app.post("/users")
def create_user(user: UserCreate):
    service.new_user(user.username, user.email, user.password)
    return {"message": "Usuário criado com sucesso"}

@app.put("/users/{user_id}")
def update_username(user_id: int, user: UserUpdate):
    service.edit_username(user_id, user.new_username)
    return {"message": "Nome de usuário atualizado com sucesso"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    service.delete_user(user_id)
    return {"message": "Usuário deletado com sucesso"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário localizado com sucesso",
            "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }}

@app.post("/tasks")
def create_task(task: TaskCreate):
    service.new_task(task.user_id, task.title, task.description)
    return {"message": "Tarefa criada com sucesso"}

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    task = service.complete_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa concluida com sucesso"}

@app.put("/tasks/{task_id}/reopen")
def reopen_task(task_id: int):
    task = service.reopen_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa reaberta com sucesso"}

@app.get("/users/{user_id}/tasks")
def get_task_by_user(user_id: int):
    tasks = service.get_tasks_by_user(user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefas localizadas com sucesso",
    "tasks": [
        {   "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "status": task.status
        }
        for task in tasks
    ]
}
    
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404,detail="Tarefa não encontrada")
    return {"message": "Tarefa localizada com sucesso",
        "task": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "status": task.status
        }
    }

@app.get("/tasks")
def get_all_tasks():
    tasks = service.get_all_tasks()
    if not tasks:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada")
    return {"message": "Tarefas localizadas com sucesso",
        "tasks": [
            {   "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            }
            for task in tasks
        ]
    }

@app.put("/tasks/{task_id}/title")
def update_task_title(task_id: int, task: TaskTitleUpdate):
    updated = service.edit_title_task(task_id, task.new_title)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Título atualizado com sucesso"}

@app.put("/tasks/{task_id}/description")
def update_task_description(task_id: int, task: TaskDescriptionUpdate):
    updated = service.edit_desc_task(task_id, task.new_description)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Descrição atualizada com sucesso"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa deletada com sucesso"}