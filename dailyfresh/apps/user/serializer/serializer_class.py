import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.user.models import User,Address
from apps.goods import models
from django_redis import get_redis_connection

from django.forms.models import model_to_dict



class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3)
    password = serializers.CharField(min_length=8)
    email = serializers.CharField()

    def validate_username(self, data):
        "验证用户名是否重复"
        result = User.objects.filter(username=data).first()
        if result:
            raise ValidationError(detail="用户名已存在")
        return data

    def validate_email(self, data):
        "局部钩子检测邮箱格式是否正确"
        regex = "^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$"
        result = re.match(regex,data)
        if not result:
            raise ValidationError(detail='邮箱格式错误')
        return data

    class Meta:
        model = User
        fields = ["username","password","email"]

class ActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_active"]


class AddressGetSerializer(serializers.ModelSerializer):
    "get只需要定制  fields 返回的字段即可"
    user = serializers.SerializerMethodField()

    def get_user(self,obj):
        dic = {
            "user_id":obj.user.id,
            "username":obj.user.username
        }
        return dic
    class Meta:
        model = Address
        fields = ["id","user","addr","is_default"]

class AddressPostSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(label="接收者",max_length=20)
    addr = serializers.CharField(label="收件信息",max_length=256)
    code = serializers.CharField(label="邮编",max_length=6,allow_null=True)
    phone = serializers.CharField(label="电话",max_length=11)#在定制的序列化器设定约束条件避免程序erro

    def phone_verify(self,phone):
        regex = r"(1[3,4,5,6,7,8,9]\d{9})"
        if not re.match(regex,phone):
            raise ValidationError("格式错误")

    def validated_phone(self,phone):
        return self.phone_verify(phone)

    class Meta:
        model = Address
        fields = ["receiver","receive_info","code","phone"]

class UserCenter_infoSerializer(serializers.ModelSerializer):
    browse_history = serializers.SerializerMethodField()

    def get_history(self,key):
        conn = get_redis_connection("default")
        sku_ids = list(map(lambda x: x.decode("utf-8"), conn.lrange(key, 0, -1)))
        queryset = models.GoodsSKU.objects.filter(id__in=sku_ids)
        return queryset

    def get_browse_history(self,obj):
        user = obj.user
        key = "history_{}".format(user.id)
        queryset = self.get_history(key)

        #redis查询浏览记录中的商品id list
        dic = [model_to_dict(obj,fields=["id","name","price","unite"]) for obj in queryset]
        return dic

    class Meta:
        model = Address
        fields = ["user","phone","address","browse_history"]