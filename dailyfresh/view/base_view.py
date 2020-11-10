#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
from apps.goods import models
from django.core.exceptions import ImproperlyConfigured

class VerifyLoginCartCountBaseView(APIView):
    """
    白名单内需要检测用户登录/购物车数量的view
    """
    def get_goods_count(self, id):
        "获取购物车商品数量"
        key = "cart_{}".format(id)
        conn = get_redis_connection("default")
        count = conn.hlen(key)
        return count

    def get_user(self, request):
        "判断是否登录"
        user = request.session.get("user")
        if not user: return None

        dic = {
            "id": user.id,
            "goods_counts": self.get_goods_count(user.id)
        }
        return dic

class CartBaseView(APIView):
    """
    添加至购物车/更新购物车
    """

    def get_count(self, **kwargs):
        return kwargs["count"]

    def get_total_count(self,conn,cart_key):
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)
        return total_count

    def update_cart(self,request):
        user = request.user_obj
        goods_id = request.POST.get("goods_id")
        count = request.POST.get("count")
        # 检测数据完整性
        if not all([goods_id, count]):
            return Response({"code": 1, "errmsg": "数据不完整"})
        # 检测商品是否存在
        obj = models.GoodsSKU.objects.filter(id=goods_id).first()
        if not obj:
            return Response({"code": 2, "errmsg": "商品不存在"})

        # 业务
        conn = get_redis_connection("default")
        cart_key = "cart_{}".format(user.id)

        #获取购物车商品数量
        cart_count = self.get_count(conn=conn,cart_key=cart_key,goods_id=goods_id,count=int(count))

        result = self.set_cache(cart_count=cart_count,conn=conn,obj=obj,cart_key=cart_key,goods_id=goods_id)
        if result:
            return result

        #获取购物车总数
        total_count = self.get_total_count(conn,cart_key)

        return {"user_id":user.id,"cart_count":conn.hlen(cart_key),"total_count":total_count}

    def set_cache(self,**kwargs):
        """
        设置缓存
        """
        if kwargs['cart_count'] > kwargs['obj'].count:
            return Response({"code": 3, "errmsg": "商品库存不足"})

        kwargs['conn'].hset(kwargs['cart_key'], kwargs['goods_id'], kwargs['cart_count'])

