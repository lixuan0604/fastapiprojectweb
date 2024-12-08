from datetime import datetime

from pydantic import BaseModel, Field
from tortoise.fields import ForeignKeyField
from typing import Union, Dict,Any

class AddProjectForm(BaseModel):
    """添加项目"""
    name: str = Field(description="项目名称", max_length=20)
    user: int = Field(description="项目负责人")

class UpdateProjectForm(BaseModel):
    """更新项目"""
    name: str = Field(description="项目名称", max_length=20)

class ProjectSchemas(BaseModel):
    """项目详情"""
    id: int = Field(description="项目id")
    name: str = Field(description="项目名称")
    user_id: int = Field(description="项目负责人")
    # 时间在申明的时候要注意类型
    create_time: datetime = Field(description="创建时间")


# ======================== 测试环境接口  ===============================
class TestEnvSchemas(BaseModel):
    id :int = Field(description="环境id")
    name:str = Field(description="环境名称")
    # create_time: datetime = Field(description="创建时间")
    host:str = Field(description="环境地址")
    global_vars:Dict[str, Any] = Field(description="全局变量",default_factory=dict)
    project_id: int = Field(description="所属项目")

class AddEnvForm(BaseModel):
    """创建测试环境"""
    name: str = Field(description="环境名称")
    host: str = Field(description="环境地址")
    global_vars: Dict[str, Any]  = Field(description="全局变量", default_factory=dict)
    project_id: int = Field( description="所属项目")

class UpdateEnvForm(BaseModel):
    """修改测试环境"""
    name: Union[str, None] = Field(..., description="环境名称")
    host: Union[str, None] = Field(..., description="环境地址")
    global_vars: Union[Dict, None] = Field(..., description="全局变量")



# ======================= 项目模块接口 ==================================
class ProjectModuleSchemas(BaseModel):
    id: int = Field(description="模块id")
    name: str = Field(description="模块名称")
    project_id: int = Field(description="所属项目")
    create_time: datetime = Field(description="创建时间")

class AddModuleForm(BaseModel):
    """创建测试"""
    project_id:int= Field(description="所属项目")
    name:str= Field(description="模块名称")

class UpdateModuleForm(BaseModel):
    """修改模块"""
    name:str= Field(description="模块名称")