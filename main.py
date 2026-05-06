from services import UserTaskService
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

service = UserTaskService()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

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
    service.new_user(user.title, user.email, user.password)
    return {"message": "Usuário criado com sucesso"}


