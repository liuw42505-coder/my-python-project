from fastapi import APIRouter, Depends, HTTPException
from schemas import UserCreate
from sqlalchemy.orm import Session
from database import SessionLocal
from models import UserDB
from auth import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/user")


# 获取数据库
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 注册
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="密码太长（最多72字符）")

    hashed_pwd = hash_password(user.password)

    db_user = UserDB(
        username=user.username,
        password=hashed_pwd
    )

    db.add(db_user)
    db.commit()

    return {"msg": "注册成功"}


# 登录
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="密码太长（最多72字符）")

    db_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    # 用 verify_password 校验
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }