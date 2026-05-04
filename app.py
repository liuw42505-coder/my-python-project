from fastapi import FastAPI
from routers import user, chat

app = FastAPI()

app.include_router(user.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"msg": "AI Chat System Running"}