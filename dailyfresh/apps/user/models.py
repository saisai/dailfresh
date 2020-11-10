from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

class User(AbstractUser,BaseModel):
    "用户表"
    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_info"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


# class AdddressManager(models.manager):
#
#     def get_default(self,user):
#         "获取默认地址"
#         # self.model:获取self对象所在的模型类
#         try:
#             address = self.get(user=user, is_default=True)  # models.Manager
#         except self.model.DoesNotExist:
#             # 不存在默认收货地址
#             address = None
#
#         return address

class Address(BaseModel):
    '用户收货信息'
    user = models.ForeignKey("User",verbose_name="所属账户")
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件信息')
    address = models.CharField(max_length=100,verbose_name="地址",default="成都市新都区西南石油大学")
    code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # objects = AdddressManager()
    def __str__(self):
        return '{}的地址'.format(self.user.username)

    class Meta:
        db_table = "address"
        verbose_name = "收货信息"
        verbose_name_plural = verbose_name
