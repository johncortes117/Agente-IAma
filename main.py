from fastapi import FastAPI
from models import User, Class



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Agente IAma"}

@app.post("/users")
async def create_user(user_data: User):
    return user_data

@app.post("/classes")
async def create_class(class_data: Class):
    return class_data