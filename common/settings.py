
# 数据库的配置信息
DATABASE = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': '123456',
    'database': 'webtest',
}

# 项目中的所以应用的models
INSTALLED_APPS = [
    'apps.users.models',
    'apps.projects.models'
]

# tortoise的基本配置
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': DATABASE
        },
    },
    'apps': {
        'models': {
            'models': ['aerich.models', *INSTALLED_APPS],
            'default_connection': 'default',
        },
    }
}

# token 配置

# 64位秘钥
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# 加密算法
ALGORITHM = "HS256"
# token 过期时间
TOKEN_TIMEOUT = 60 * 60 * 24 *7



