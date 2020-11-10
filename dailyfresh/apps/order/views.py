
import os

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.response import Response

from django.forms import model_to_dict
from django_redis import get_redis_connection

from apps.goods.models import GoodsSKU
from apps.order import models
from apps.user.models import Address

from utils.transform import bytes_to_dic
from apps.order.serializer.order_serializer import OrderSerializers

from apps.order.filter.order_filter import UserCenterFilter
from apps.order.serializer.order_serializer import UserCenterOrderSerializer


from django.conf import settings

from apps.order.utils.alipay_obj import AliPayObj

class OrderIndexView(APIView):
    """
    订单首页
    post:goods_list/
    """
    def get(self,request):
        user = request.user_obj
        cart_key = "cart_{}".format(user.id)

        conn = get_redis_connection("default")
        query_dic = bytes_to_dic(conn.hgetall(cart_key))


        obj_list = list()
        for i in query_dic.items():
            obj = GoodsSKU.objects.filter(id=i[0]).first()
            obj_dic = model_to_dict(obj, fields=['id', 'name', 'unite', 'price', 'buy_count'])
            obj_dic['buy_count'] = i[1]
            obj_list.append(obj_dic)


        dic = {
            "addr":[{'id':addr.id,'addr':addr.addr}for addr in Address.objects.filter(user=user)],
            "goods_list":obj_list,
            "pay_method":[{each[0]:each[1]} for each in models.OrderInfo.PAY_METHOD_CHOICES],
            "tansit_price":10,
        }

        return Response(dic)



class CreateOrderView(CreateAPIView):
    """
    创建订单
    method：ajax_post
    params: addr_id/pay_id/商品id列表
    todo 关于商品状态的验证/商品下架购物车如何处理/商品下架之 redis购物车处理+下单处理
    todo 序列化外键的查询和校验/自定义字段
    todo 接口的幂等性
    todo 字典的key数据类型一定要一致
    todo 需要简化下代码
    todo 自定义超链接
    """
    serializer_class = OrderSerializers
    queryset = models.OrderInfo.objects


class UserCenterOrder(ListAPIView):
    """
    用户中心-订单
    分类:已支付/未支付

    """
    serializer_class = UserCenterOrderSerializer
    queryset = models.OrderInfo.objects
    filter_backends = [UserCenterFilter,]

class OrderPayView(APIView):
    '''订单支付'''

    def get_alipay_obj(self,request):
        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return Response({'res': 1, 'errmsg': '无效的订单id'})

        try:
            order = models.OrderInfo.objects.get(
                order_id=order_id,
                user=request.user_obj,
                pay_method=3,
                order_status=1)
        except models.OrderInfo.DoesNotExist:
            return Response({'res': 2, 'errmsg': '订单不存在'})
        # 业务处理:使用python sdk调用支付宝的支付接口
        # 初始化
        alipay = AliPayObj(
            appid="2016103100782375",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
            alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        return {'alipay':alipay,'order':order}


    def post(self, request):

        result = self.get_alipay_obj(request)
        if type(result)!=dict:
            return result
        alipay = result['alipay']
        order = result['order']

        # 调用支付接口
        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        total_pay = order.total_price+order.transit_price # Decimal
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_id, # 订单id
            total_amount=str(total_pay), # 支付总金额
            subject='测试订单%s'%order.order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        # 返回应答
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return Response({'res':3, 'pay_url':pay_url})


class CheckPayView(OrderPayView):
    '''查看订单支付的结果'''
    def post(self, request):
        '''查询支付结果'''

        result = self.get_alipay_obj(request)
        if type(result) != dict:
            return result
        alipay = result['alipay']
        order = result['order']

        # 调用支付宝的交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(order.order_id)
            code = response.get('code')

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                # 更新订单状态
                order.trade_no = trade_no
                order.order_status = 4 # 待评价
                order.save()
                # 返回结果
                return Response({'res':3, 'message':'支付成功'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # 等待买家付款
                # 业务处理失败，可能一会就会成功
                import time
                time.sleep(5)
                continue
            else:
                # 支付出错
                print(code)
                return Response({'res':4, 'errmsg':'支付失败'})

#Todo 退款
