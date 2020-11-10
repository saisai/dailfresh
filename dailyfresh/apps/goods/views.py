from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from apps.goods import models
from django.forms import model_to_dict
from view.base_view import VerifyLoginCartCountBaseView




class GetIndexDataView(VerifyLoginCartCountBaseView):

    def get_goods_info(self):
        "获取商品数据"
        query = models.GoodsType.objects.all()
        lis = [{each.id: {"name": each.name,
                          "goods":
                              [model_to_dict(i, exclude=["is_delete", "type", "spu"]) for i in
                               models.GoodsSKU.objects.filter(type=each)]
                          }} for each in query]

        return lis

    def get(self, request):
        dic = {
            "user": self.get_user(request),
            "goods_info": self.get_goods_info()
        }

        return Response(dic)


class GetGoodsListView(ListAPIView):
    """
    该类型下所有sku:
        sku_id/name/price/单位
    排序方式:
        默认/价格/销量

    todo type:[{id:,name:,}]
    todo 商品分页 需要与前端协商一页放几个
    todo 用户登录信息没返回
    todo 应该使用url传参
    """
    from apps.goods.serializers.goods_serializers import GoodsTypeListserializer
    from apps.goods.filter.goods_filter import GoodsTypeFilter

    queryset = models.GoodsSKU.objects
    serializer_class = GoodsTypeListserializer
    filter_backends = [GoodsTypeFilter,]
    # pagination_class =


class GetGoodsView(VerifyLoginCartCountBaseView):
    """
    需要查询商品是否存在/
    查询商品状态
    获取单品信息:
        sku: sku_id/name/price/单位/count/描述
        同spu其他产品: id/name
        spu: spu_id/name/商品介绍/
        新品推荐(2): 该商品类型下推荐其他单品
        cart_count:
        type:[
            {id:,name:,}
        ]
    接口:
        1.add_cart
        2.buy
        3.comment
    todo: 1.商品状态 / 2.buy / 3.comment
    todo 应该使用url传参
    """

    def get_return(self, request, goods_obj):
        dic = {
            "user": self.get_user(request),
            "goods_type": [model_to_dict(i, fields=["id","name"]) for i in models.GoodsType.objects.all()],
            "goods_info": model_to_dict(goods_obj, exclude=["status", 'spu']),
            "others": [model_to_dict(v, fields=["id", "name"]) for v in
                       models.GoodsSKU.objects.filter(spu=goods_obj.spu).
                           exclude(id=goods_obj.id)],
            "new_products": [
                model_to_dict(c,fields=["id","name","price"])
                for c in models.GoodsSKU.objects.filter(type=goods_obj.type).order_by("-create_time")[:2]
            ],
            "comment":{

            }
        }
        return dic

    def get(self, request):
        id = request.query_params["goods_id"]
        query = models.GoodsSKU.objects.filter(pk=id)
        if not query: return Response({
            "goods": None,
        })
        goods_obj = query.first()
        return Response(self.get_return(request, goods_obj))





