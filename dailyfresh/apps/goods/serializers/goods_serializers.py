#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers
from apps.goods import models

class GoodsTypeListserializer(serializers.ModelSerializer):


    class Meta:
        model = models.GoodsSKU
        fields = ["id","name","price","unite"]