from django.db import models
from db.base_model import BaseModel


# class GoodsImage(BaseModel):
#     "单品图片"
#     sku = models.ForeignKey("GoodsSKU",verbose_name="单品")
#     # image = models.ImageField(upload_to='goods', verbose_name='图片路径')
#     is_default = models.BooleanField(default=False,verbose_name="是否为默认图片")
#
#     class Meta:
#         db_table = "GoodsImage"
#         verbose_name = "商品图片"
#         verbose_name_plural = verbose_name

class GoodsType(BaseModel):
    "商品种类"
    name = models.CharField(max_length=20,verbose_name="种类名称")
    # logo = models.CharField(max_length=20,verbose_name="首页种类logo")
    # index_img = models.ImageField(upload_to='type', verbose_name='类型图片')

    class Meta:
        db_table = "GoodsType"
        verbose_name = "商品种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSPU(BaseModel):
    "商品SPU"
    name = models.CharField(max_length=20,verbose_name="商品名称")
    detail = models.CharField(max_length=256,verbose_name="SPU商品描述")

    class Meta:
        db_table = "GoodsSPU_info"
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSKU(BaseModel):
    "单品信息"
    name = models.CharField(max_length=20,verbose_name="单品名称")
    detail = models.CharField(max_length=256,verbose_name="单品描述")
    price = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='商品价格')
    count = models.IntegerField(default=1,verbose_name="库存")
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    status_choices={
        (0 ,"下架"),
        (1 ,"上线"),
        (2 ,"售罄")
    }
    status  = models.SmallIntegerField(choices=status_choices,default=1,verbose_name="商品状态")
    sales = models.IntegerField(default=0,verbose_name="销售数量")
    # image = models.ImageField(upload_to='goods', verbose_name='商品图片',null=True)
    type = models.ForeignKey("GoodsType",verbose_name="商品种类")
    spu = models.ForeignKey("GoodsSPU",verbose_name="商品SPU")

    class Meta:
        db_table = "Goods_info"
        verbose_name = "单品信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name