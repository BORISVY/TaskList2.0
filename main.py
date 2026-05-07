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
    title: str
    description: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    user = service.login(data.username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {
        "message": "Login realizado com sucesso",
        "user": {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }
    }

@app.post("/users")
def create_user(user: UserCreate):
    service.new_user(user.username, user.email, user.password)
    return {"message": "Usuário criado com sucesso"}

@app.put("/users/{user_id}")
def update_username(user_id, user: UserUpdate):
    service.edit_username(user_id, user.new_username)
    return {"message": "Nome de usuário atualizado com sucesso"}

@app.delete("/users/{user_id}")
def delete_user(user_id):
    service.delete_user(user_id)
    return {"message": "Usuário deletado com sucesso"}

@app.get("/users/{user_id}")
def get_user(user_id):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário localizado com sucesso",
            "user": {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }}