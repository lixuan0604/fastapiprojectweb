
from tortoise import models, fields

class TestProject(models.Model):
    """测试项目表"""
    id = fields.IntField(description="项目id", primary_key=True)
    name = fields.CharField(max_length=50, description="项目名称")
    user = fields.ForeignKeyField("models.Users",related_name="projects", description="负责人")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建日期")

    def __str__(self):
        return self.name

    class Meta:
        table = "test_project"
        table_description = "测试项目表"


class TestEnv(models.Model):
    """测试环境表"""
    id = fields.IntField(description="环境id", primary_key=True)
    # envs 反向访问的字段
    project = fields.ForeignKeyField('models.TestProject', description="所属项目", related_name="envs")
    global_variable = fields.JSONField(description="全局变量", default=dict, null=True, blank=True)
    name = fields.CharField(description="测试环境名称", max_length=50)
    host = fields.CharField(description="测试环境的host地址", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        table = "test_env"
        table_description = "测试环境表"


class ProjectModule(models.Model):
    """功能模块表"""
    id = fields.IntField(description="模块id", primary_key=True)
    name = fields.CharField(max_length=50, description="模块名称")
    project = fields.ForeignKeyField('models.TestProject', description="所属项目", related_name="modules")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建日期")

    def __str__(self):
        return self.name

    class Meta:
        table = "project_module"

