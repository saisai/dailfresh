from rest_framework.filters import BaseFilterBackend
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU



class CartFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user_obj
        #建立redis连接
        conn = get_redis_connection("default")
        cart_key = "cart_{}".format(user.id)

        #dic封装在request中以供序列化使用
        cart_dict = conn.hgetall(cart_key)
        if not cart_dict: return None

        dic = {}
        for i in cart_dict.items():
            dic[i[0].decode("utf-8")] = i[1].decode()
        request.cart_dic = dic

        #批量查询
        cart_goods = GoodsSKU.objects.in_bulk(cart_dict.keys()).values()
        return cart_goods