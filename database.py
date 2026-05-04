from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite数据库（本地文件）
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ai_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)