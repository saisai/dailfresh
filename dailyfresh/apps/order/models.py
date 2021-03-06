from django.db import models
from db.base_model import BaseModel



class OrderInfo(BaseModel):
    """
    订单信息表
    """
    user = models.ForeignKey('user.User',verbose_name="用户")
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name="订单id")
    addr = models.ForeignKey('user.Address',verbose_name="用户收货地址")
    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES,verbose_name='支付方式',default=3)
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价',default=0)
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单运费')
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_no = models.CharField(max_length=128, default='', verbose_name='支付编号')

    class Meta:
        db_table = 'order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

class OrderGoods(BaseModel):
    """
    订单商品表
    """
    order = models.ForeignKey('OrderInfo', verbose_name='订单信息')
    sku = models.ForeignKey('goods.GoodsSKU', verbose_name='具体商品')
    count = models.IntegerField(default=1, verbose_name='商品数目')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    comment = models.CharField(max_length=256, default='', verbose_name='评论')

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name