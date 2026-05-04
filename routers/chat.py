from fastapi import APIRouter
from schemas import ChatRequest
from database import SessionLocal
from models import ChatDB
from openai import OpenAI

router = APIRouter(prefix="/chat")

client = OpenAI(
    api_key="sk-hvPfCi0ZQ9y5XXGPoUWL5mjlac67h9q0J2FTJ0Y13QCOHmon",
    base_url="https://api.moonshot.cn/v1"
)

def real_ai_answer(question: str):
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content

@router.post("/")
def chat(req: ChatRequest):
    db = SessionLocal()

    answer = real_ai_answer(req.question)

    chat_record = ChatDB(
        question=req.question,
        answer=answer
    )

    db.add(chat_record)
    db.commit()
    db.close()

    return {"answer": answer}