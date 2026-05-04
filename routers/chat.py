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
    db = SessionLocal()

    answer = real_ai_answer(req.question)

    chat_record = ChatDB(
        question=req.question,
        answer=answer,
        user_id=user["user_id"]   # ⭐ 关键！
    )

    db.add(chat_record)
    db.commit()
    db.close()

    return {
        "answer": answer
    }

@router.get("/history")
def get_history(user=Depends(get_current_user)):
    """
    Depends 是 FastAPI 的依赖注入系统（Dependency Injection）的核心工具。
    基本概念：
    依赖注入：一种设计模式，用于管理代码之间的依赖关系
    作用：自动执行某些函数，并将结果传递给路由函数
    好处：代码复用、解耦、易于测试
    """
    db = SessionLocal()

    records = db.query(ChatDB).filter(
        ChatDB.user_id == user["user_id"]
    ).all()

    db.close()

    return records
"""
客户端请求                         FastAPI 服务器
    |                                    |
    |  GET /chat/history                 |
    |  Authorization: Bearer eyJ...      |
    | ────────────────────────────────>  |
    |                                    |
    |                          看到 Depends(get_current_user)
    |                                    |
    |                          执行 get_current_user():
    |                            1. 提取 token
    |                            2. 验证签名
    |                            3. 检查过期
    |                                    |
    |                          ┌──── 验证成功? ────┐
    |                          ↓                   ↓
    |                     ✅ 有效              ❌ 无效
    |                          ↓                   ↓
    |                    返回用户信息         抛出 401 错误
    |                    {"user_id": 1}     {"detail": "无效的token"}
    |                          ↓                   ↓
    |                    继续执行路由          直接返回错误
    |                    业务逻辑              
    |                          ↓                   
    |  {"chats": [...]}        |
    | <────────────────────────|

"""