from database import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password = Column(String(100))

class ChatDB(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255))
    answer = Column(String(255))

    # ⭐ 新增这一行
    user_id = Column(Integer, ForeignKey("users.id"))

# 创建表
Base.metadata.create_all(bind=engine)
"""
ORM（Object-Relational Mapping，对象关系映射） 是一种编程技术，用于在面向对象编程语言和关系型数据库之间建立映射关系。
Python 面向对象世界          关系型数据库世界
━━━━━━━━━━━━━━━━━━━━      ━━━━━━━━━━━━━━━━━━━━
类 (Class)        ←→      表 (Table)
对象 (Object)     ←→      行 (Row)
属性 (Attribute)  ←→      列 (Column)
无需写 SQL
数据库无关性
类型安全
安全性更高
代码更清晰
"""

