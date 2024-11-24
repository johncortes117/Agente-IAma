from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
    country: str

class Class(BaseModel):
    name: str
    user: User
    grade: float