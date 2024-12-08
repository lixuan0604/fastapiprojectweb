from tortoise import models,fields

class Users(models.Model):
    id = fields.IntField(pk=True,auto_increment=True )
    username = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255,default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=False)
    mobile = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        table = "users"
        table_description = "用户表"
