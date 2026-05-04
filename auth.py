from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 密钥（随便写一串，但项目里要固定）
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
CryptContext: 这是 passlib 库中的一个类，用于管理密码哈希算法
schemes=["bcrypt"]: 指定使用 bcrypt 算法来加密密码
bcrypt 是一种安全的密码哈希算法，具有盐值（salt）机制
能有效防止彩虹表攻击和暴力破解
deprecated="auto": 自动处理过时的哈希算法
当检测到使用旧算法生成的密码时，会自动重新哈希为新算法
"""

# 加密密码
def hash_password(password: str):
    return pwd_context.hash(password)


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 创建 token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
"""
JWT (JSON Web Token) 是一种开放标准（RFC 7519），用于在各方之间安全地传输信息
由三部分组成（用.分隔）：
Header（头部） - 加密算法和令牌类型
Payload（载荷） - 实际数据
Signature（签名） - 验证令牌完整性

jwt.encode() 是 python-jose 库中的函数，用于创建 JWT token。

参数 1: to_encode (payload/载荷)
参数 2: SECRET_KEY (密钥)
参数 3: algorithm=ALGORITHM (算法)
"""

security = HTTPBearer()
"""1. 什么是 HTTPBearer？
这是 fastapi.security 模块中的一个类
用于从 HTTP 请求头中提取 Bearer Token
遵循 OAuth 2.0 的 Bearer Token 规范

当客户端发送请求时，需要在请求头中包含 token:uthorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
HTTPBearer() 会自动：
从 Authorization 请求头中提取 token
验证格式是否正确
将 token 传递给依赖函数

"""

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    HTTPAuthorizationCredentials 是 FastAPI 提供的一个数据类（Data Class），用于存储从 HTTP 请求头中提取的认证信息。
    HTTPAuthorizationCredentials 对象的属性
        credentials.credentials  # 实际的 token 字符串
        credentials.scheme       # 认证方案（如 "Bearer"）
    Bearer 认证是一种基于令牌（Token）的 HTTP 认证方式，遵循 RFC 6750 标准。
    Authorization: Bearer <token>
    Bearer：表示"持有者"，意思是"持有这个 token 的人就是合法用户"
    <token>：实际的认证令牌（在您的项目中是 JWT）
    客户端                          服务器
  |                               |
  |--- 1. 登录请求 -------------->|
  |    (用户名/密码)               |
  |                               |
  |<-- 2. 返回 Token -------------|
  |    {"token": "eyJ..."}        |
  |                               |
  |--- 3. 携带 Token 请求 -------->|
  |    Authorization: Bearer ...  |
  |                               |
  |<-- 4. 验证通过，返回数据 ------|
  |                               |

    """
    token = credentials.credentials
    """
    try-except 是 Python 中的异常处理机制（也称为错误处理），用于捕获和处理程序运行时可能出现的错误
    raise 是因为在 FastAPI 依赖函数中，我们需要通过抛出异常来中断请求并返回错误响应
    ❌ 使用 return（不正确）：
        def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            # 这样只会返回一个异常对象，不会中断请求
            return HTTPException(status_code=401, detail="无效的token")
    路由函数会继续执行
    用户可能拿到的是异常对象而不是错误响应
    无法正确设置 HTTP 状态码
    ✅使用 raise（正确）：
        def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            # 立即中断请求，返回 401 错误响应
            raise HTTPException(status_code=401, detail="无效的token")
    立即中断请求处理
    FastAPI 自动捕获并转换为 HTTP 响应
    正确设置状态码和响应体
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        """
        jwt.decode() 用于解码和验证 JWT token，将 token 字符串转换回原始的字典数据
        decode 函数的三个参数：
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #                            ^^^^^   ^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^
    #                            token      密钥         算法列表
        """
        """
            return payload
             ↓ 返回用户信息
               例如: {"user_id": 1, "exp": 1705312245}
           """
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="无效的token")
