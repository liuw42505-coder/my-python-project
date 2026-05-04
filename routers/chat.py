from fastapi import APIRouter
from schemas import ChatRequest
from database import SessionLocal
from models import ChatDB
from openai import OpenAI
from auth import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/chat")

client = OpenAI(
    api_key="sk-hvPfCi0ZQ9y5XXGPoUWL5mjlac67h9q0J2FTJ0Y13QCOHmon",
    base_url="https://api.moonshot.cn/v1"
)


def real_ai_answer(question: str):
    """
    调用Moonshot AI API获取问题的真实回答
    
    Args:
        question (str): 用户提出的问题
        
    Returns:
        str: AI生成的回答内容
    """
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content


@router.post("/")
def chat(req: ChatRequest, user=Depends(get_current_user)):
    """
    处理聊天请求，调用AI获取回答并保存聊天记录
    
    Args:
        req (ChatRequest): 聊天请求对象，包含用户问题
        user: 当前用户信息（通过依赖注入获取）
        
    Returns:
        dict: 包含AI回答和用户信息的字典，格式为：
              {
                  "answer": str,  # AI生成的回答
                  "user": object  # 当前用户信息
              }
    """
    db = SessionLocal()

    answer = real_ai_answer(req.question)

    chat_record = ChatDB(
        question=req.question,
        answer=answer
    )

    db.add(chat_record)
    db.commit()
    db.close()

    return {
        "answer": answer,
        "user": user
    }