import datetime

from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework.serializers import ValidationError

from apps.order import models
from apps.user.models import Address
from apps.goods.models import GoodsSKU

from django.forms import model_to_dict

from utils.transform import bytes_to_dic

# django事务
from django.db import transaction


class OrderSerializers(serializers.ModelSerializer):

    def validate(self, attrs):
        request = self.context['request']
        data = request.data
        addr_id = data['addr_id']
        goods_list = data['goods_list'].split(',')

        # 查询是否为该用户的收货地址
        if not Address.objects.filter(id=addr_id,user=request.user_obj):
            raise ValidationError("收货地址不存在")

        # attrs['obj'] = dict()
        attrs['addr_id'] = int(addr_id)
        attrs['goods_list'] = goods_list

        return attrs

    def create_order_goods(self,goods_list,save_id,dic,total_price,order_obj,conn,user_id):
        for i in goods_list:
            # goods exists?
            for times in range(3):
                try:
                    goods_obj = GoodsSKU.objects.get(id=i)
                except Exception as e:
                    transaction.savepoint_rollback(save_id)
                    raise ValidationError('goods is not exists!')

                # Calculate product count
                goods_count = dic.get(i)
                # GOODSID in redis?
                if not goods_count:
                    transaction.savepoint_rollback(save_id)
                    raise ValidationError('{}商品不存在于您的购物车中!'.format(goods_obj.name))
                # 库存
                if goods_obj.count < goods_count:
                    transaction.savepoint_rollback(save_id)
                    raise ValidationError('库存不足!')
                #  all goods price
                total_price += goods_obj.price * goods_count

                count = goods_obj.count - goods_count
                sales = goods_obj.sales + goods_count
                res = GoodsSKU.objects.filter(id=goods_obj.id, count=goods_obj.count).update(count=count, sales=sales)

                if not res:
                    if times == 2:
                        transaction.savepoint_rollback(save_id)
                        raise ValidationError('')
                    continue

                # create order_goods data
                models.OrderGoods.objects.create(
                    order=order_obj,
                    sku=goods_obj,
                    count=goods_count,
                    price=goods_obj.price,
                )

                # clear goods_id in redis
                conn.hdel('cart_{}'.format(user_id), i)
                break

        # update all goods_price
        order_obj.total_price = total_price
        order_obj.save()



    @transaction.atomic()
    def create(self, validated_data):
        # goods_list
        goods_list = validated_data['goods_list']
        #从validated_data中去除
        validated_data.pop('goods_list')

        request = self.context['request']
        user = request.user_obj
        # 创建订单号
        user_id = user.id
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        # 获取购物车
        conn = get_redis_connection('default')
        redis_dic = conn.hgetall('cart_{}'.format(user_id))
        dic = bytes_to_dic(redis_dic)
        #计算购物车总数
        total_count = sum(dic.values())
        total_price = 0
        tansit = 10

        #  保存字段信息/创建订单信息
        validated_data.update({
            'user': user,
            'order_id': order_id,
            'total_count': total_count,
            'transit_price': tansit,
        })

        # 设置事务保存点
        save_id = transaction.savepoint()
        try:
        # create_order_data
            order_obj = models.OrderInfo.objects.create(**validated_data)
            self.create_order_goods(goods_list,save_id,dic,total_price,order_obj,conn,user_id)

        except Exception as e:
            transaction.savepoint_rollback(save_id)
            raise ValidationError(e)
        # 提交事务
        transaction.savepoint_commit(save_id)

        return order_obj

    class Meta:
        model = models.OrderInfo
        fields = ["pay_method"]

class UserCenterOrderSerializer(serializers.ModelSerializer):

    goods = serializers.SerializerMethodField()
    order_status = serializers.CharField(source='get_order_status_display')
    # Link = serializers.SerializerMethodField()

    def get_goods(self,obj):
        order_goods = models.OrderGoods.objects.filter(order_id=obj.order_id)
        goods_list = []
        print(order_goods)
        for i in order_goods:
            dic={
                'name':i.sku.name,
                'price':i.sku.price,
                'unite':i.sku.unite,
                'count':i.count
            }
            goods_list.append(dic)
        return goods_list


    class Meta:
        model = models.OrderInfo
        fields = ['create_time','order_id','order_status','total_price','goods']