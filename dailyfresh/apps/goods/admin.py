from django.contrib import admin
from apps.goods import models
# admin中注册 表
admin.site.register([models.GoodsType,models.GoodsSPU,models.GoodsSKU])
