from rest_framework.response import Response
from view.base_view import CartBaseView
from rest_framework.generics import ListAPIView
from apps.goods.models import GoodsSKU
from apps.cart.serializer.cart_serializer import CartSerializers
from apps.cart.filter.cart_filter import CartFilterBackend

class AddGoodsView(CartBaseView):
    """
    添加商品到购物车
    请求方式:Post
    商品详情页/商品列表页
    在未知购物车该商品实际数量前提下，添加
    """
    def get_count(self,**kwargs):
        conn = kwargs["conn"]
        cart_key = kwargs["cart_key"]
        goods_id = kwargs["goods_id"]
        count = kwargs["count"]

        # 购物车商品数量是否超出库存？
        exist_count = conn.hget(cart_key, goods_id)
        # 购物车是否含有该商品？
        if not exist_count: exist_count = 0
        cart_count = int(exist_count) + count
        return cart_count

    def post(self, request):
        result = self.update_cart(request)
        if type(result)!= dict:return result
        dic = {
            "code": 6,
            "msg": 'ok',
            "data": {
                "user_id": result["user_id"],
                "cart_count": result["cart_count"]
            }
        }
        return Response(dic)


class Update_CartView(CartBaseView):
    """
    更新购物车商品数量
    +/-
    请求方式:ajax_post
    """

    def post(self,request):
        result = self.update_cart(request)
        if type(result) != dict: return result
        dic = {
            "code": 6,
            "msg": 'ok',
            "data": {
                "user_id": result["user_id"],
                "total_count": result["total_count"]
            }
        }
        return Response(dic)

class Del_cartView(CartBaseView):
    """
    删除商品
    请求方式:ajax_post
    todo 不需要传递count数量
    todo 重复的操作合并化
    """
    def set_cache(self,**kwargs):
        kwargs["conn"].hdel(kwargs['cart_key'],kwargs["goods_id"])
    def post(self,request):
        result = self.update_cart(request)
        if type(result) != dict: return result
        dic = {
            "code": 6,
            "msg": '删除成功',
            "data": {
                "user_id": result["user_id"],
                "total_count": result["total_count"]
            }
        }
        return Response(dic)

class CartView(ListAPIView):
    '''
    购物车页面数据
    '''
    queryset = GoodsSKU.objects
    serializer_class = CartSerializers
    filter_backends = [CartFilterBackend,]
