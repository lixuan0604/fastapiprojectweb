from fastapi import APIRouter, HTTPException, Depends
from typing import List, Union
from apps.projects.models import TestProject, TestEnv, ProjectModule
from apps.projects.schemas import AddProjectForm, ProjectSchemas, UpdateProjectForm, AddEnvForm, TestEnvSchemas, \
    UpdateEnvForm, ProjectModuleSchemas, AddModuleForm, UpdateModuleForm
from apps.users.models import Users
from common.auth import is_authenticated

# 创建路由对象
router = APIRouter(prefix="/api/pro")


@router.post("/projects", tags=["项目"], summary="创建项目", status_code=201)
async def create_project(item: AddProjectForm, user_info: dict = Depends(is_authenticated)):
    # 根据用户ID查询用户
    user = await Users.get_or_none(id=item.user)
    if not user:
        raise HTTPException(status_code=422, detail="用户不存在")
    if user.id != user_info["id"]:
        raise HTTPException(status_code=400, detail="用户只能给自己创建项目")
    # 创建项目
    pro = await TestProject.create(name=item.name, user=user)
    return pro


@router.delete("/projects/{id}/", tags=["项目"], summary="删除项目", status_code=204)
async def delete_project(id: int, user_info: dict = Depends(is_authenticated)):
    """删除项目"""
    project = await TestProject.get_or_none(id=id).prefetch_related("user")
    if not project:
        raise HTTPException(status_code=422, detail="项目不存在")
    if project.user.id != user_info["id"]:
        raise HTTPException(status_code=400, detail="用户只能删除自己创建的项目")
    await project.delete()
    return {"detail": "删除成功"}


@router.put("/projects/{id}/", tags=["项目"], summary="修改项目", status_code=200, response_model=ProjectSchemas)
async def update_project(id: int, item: UpdateProjectForm, user_info: dict = Depends(is_authenticated)):
    """修改项目"""
    pro = await TestProject.get_or_none(id=id).prefetch_related("user")
    if not pro:
        raise HTTPException(status_code=422, detail="项目不存在")
    if pro.user.id != user_info["id"]:
        raise HTTPException(status_code=400, detail="用户只能修改自己创建的项目")
    pro.name = item.name
    await pro.save()
    return pro


@router.get("/projects/", tags=["项目"], summary="获取项目列表", status_code=200, response_model=List[ProjectSchemas])
async def get_projects(user_info: dict = Depends(is_authenticated)):
    # 每个用户只能看到自己创建的项目
    user = await Users.get_or_none(id=user_info["id"])
    if not user:
        raise HTTPException(status_code=422, detail="用户不存在")
    projects = await TestProject.filter(user=user).all()
    return projects


@router.get("/projects/{id}", tags=["项目"], summary="获取单个项目详情", response_model=ProjectSchemas)
async def get_projects(id: int, user_info: dict = Depends(is_authenticated)):
    # 获取单个项目
    project = await TestProject.get_or_none(id=id)
    if not project:
        raise HTTPException(status_code=422, detail="项目不存在")
    return project


#  ============================================测试环境接口=============================
@router.post('/envs', tags=['测试环境管理'], summary='创建测试环境', status_code=201, response_model=TestEnvSchemas)
async def create_env(item: AddEnvForm, user_info: dict = Depends(is_authenticated)):
    project = await TestProject.get_or_none(id=item.project_id)
    if not project:
        raise HTTPException(status_code=422, detail="项目不存在")
    # env = await  TestEnv.create(**item.dict())
    env = await TestEnv.create(name=item.name, host=item.host, global_vars=item.global_vars, project_id=item.project_id)
    return env


@router.put('/envs/{id}', tags=['测试环境管理'], summary='修改测试环境', response_model=TestEnvSchemas)
async def update_env(id: int, item: UpdateEnvForm, user_info: dict = Depends(is_authenticated)):
    env = await TestEnv.get_or_none(id=id)
    if not env:
        raise HTTPException(status_code=422, detail="环境不存在")
    # exclude_unset=True  只修改传递了的字段
    env = await env.update_from_dict(item.dict(exclude_unset=True))
    await env.save()
    return env


@router.delete('/envs/{id}', tags=['测试环境管理'], summary='删除测试环境', status_code=204)
async def delete_env(id: int, user_info: dict = Depends(is_authenticated)):
    env = await TestEnv.get_or_none(id=id)
    if not env:
        raise HTTPException(status_code=422, detail="环境不存在")
    await env.delete()


@router.get('/envs', tags=['测试环境管理'], summary='获取测试环境列表', response_model=List[TestEnvSchemas])
async def get_envs(project: Union[int, None] = None, user_info: dict = Depends(is_authenticated)):
    query = TestEnv.all()
    if project:
        project = await TestProject.get_or_none(id=project)
        query = query.filter(project=project)
    envs = await query
    return envs


# 获取单个测试环境详情
@router.get('/envs/{id}', tags=['测试环境管理'], summary='获取单个测试环境详情', response_model=TestEnvSchemas)
async def get_env(id: int, user_info: dict = Depends(is_authenticated)):
    env = await TestEnv.get_or_none(id=id)
    if not env:
        raise HTTPException(status_code=422, detail="环境不存在")
    return env


#  ============================================项目下模块管理接口=============================

@router.post('/modules', tags=['测试模块管理'], summary='创建测试模块', status_code=201,
             response_model=ProjectModuleSchemas)
async def create_module(item: AddModuleForm, user_info: dict = Depends(is_authenticated)):
    project = await TestProject.get_or_none(id=item.project_id)
    if not project:
        raise HTTPException(status_code=422, detail="传入的项目ID不存在")
    module = await ProjectModule.create(name=item.name, project=project)
    return module

@router.put('/modules/{id}', tags=['测试模块管理'], summary='修改测试模块', response_model=ProjectModuleSchemas)
async def update_module(id: int, item: UpdateModuleForm, user_info: dict = Depends(is_authenticated)):
    module = await ProjectModule.get_or_none(id=id)
    if not module:
        raise HTTPException(status_code=422, detail="模块不存在")
    module.name = item.name
    await module.save()
    return module

@router.delete('/modules/{id}', tags=['测试模块管理'], summary='删除测试模块', status_code=204)
async def delete_module(id: int, user_info: dict = Depends(is_authenticated)):
    module = await ProjectModule.get_or_none(id=id)
    if not module:
        raise HTTPException(status_code=422, detail="模块不存在")
    await module.delete()


@router.get('/modules', tags=['测试模块管理'], summary='获取测试模块列表', response_model=List[ProjectModuleSchemas])
async def get_modules(project: Union[int, None] = None, user_info: dict = Depends(is_authenticated)):
    query = ProjectModule.all()
    if project:
        project = await TestProject.get_or_none(id=project)
        query = query.filter(project=project)
    modules = await query
    return modules


@router.get('/modules/{id}', tags=['测试模块管理'], summary='获取单个测试模块详情', response_model=ProjectModuleSchemas)
async def get_module(id: int, user_info: dict = Depends(is_authenticated)):
    module = await ProjectModule.get_or_none(id=id)
    if not module:
        raise HTTPException(status_code=422, detail="模块不存在")
    return module
