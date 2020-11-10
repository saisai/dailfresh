from apps.goods.models import GoodsSKU
from rest_framework import serializers

class CartSerializers(serializers.ModelSerializer):
    goods_count = serializers.SerializerMethodField()

    def get_goods_count(self,obj):
        request = self.context['request']
        count = request.cart_dic.get(str(obj.id))
        return count

    class Meta:
        model = GoodsSKU
        fields = ['name',"id",'price','unite',"goods_count"]