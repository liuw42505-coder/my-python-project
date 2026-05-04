from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    question: str