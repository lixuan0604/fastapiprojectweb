from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    username: str = Field(description="用户名", min_length=6, max_length=20)
    password: str = Field(description="密码", min_length=6, max_length=18)


class RegisterForm(LoginForm):
    password_confirm: str = Field(description="确认密码", min_length=6, max_length=18)
    email: str = Field(description="邮箱")
    mobile: str = Field(description="手机号")
    nickname: str = Field(default='', description="昵称")


# 返回的用户信息
class UserInfoSchema(BaseModel):
    id: int = Field(description="用户id")
    username: str = Field(description="用户名")
    nickname: str = Field(description="昵称")
    email: str = Field(description="邮箱")
    mobile: str = Field(description="手机号")
    is_active: bool = Field(description="是否激活")
    is_superuser: bool = Field(description="是否超级管理员")


# 登录成功后返回的数据
class LoginSchema(BaseModel):
    token: str = Field(description="访问令牌")
    user: UserInfoSchema


class TokenForm(BaseModel):
    token: str


class Token(BaseModel):
    """接口文档的使用"""
    access_token: str
    token_type: str
