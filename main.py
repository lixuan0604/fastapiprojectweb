from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from apps.users.api import router as user_router
from apps.projects.api import router as pro_router

from common import settings

app = FastAPI(title="Web测试平台接口文档",
              description="FastAPI",
              version="0.0.1")

# 注册ORM模型
register_tortoise(app,
                  config=settings.TORTOISE_ORM,
                  modules={"models": ["models"]},
                  )


app.include_router(user_router)
app.include_router(pro_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
