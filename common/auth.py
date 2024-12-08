"""
用于用户认证和权限校验的公共模块
安装依赖：
    pip install passlib[bcrypt]
    pip install pyjwt

"""
from passlib.context import CryptContext
import time
import jwt
from common import settings
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

# 获取请求头中的token
async def is_authenticated(token:str = Depends(oauth2_scheme)) ->dict:
    """校验token 获取用户信息"""
    return verify_token(token)

def create_token(userinfo: dict):
    # 过期时间
    expire = int(time.time()) + settings.TOKEN_TIMEOUT
    userinfo['exp'] = expire
    # 使用pyjwt生成token
    return jwt.encode(userinfo, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token):
    """校验token"""
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return data
    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=401,detail="token过期")




def get_password_hash(password):
    """
    哈希密码
    :param password: 明文密码
    :return:
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    校验密码
    :param plain_password: 明文密码
    :param hashed_password: 密文密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

