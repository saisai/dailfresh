#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.filters import BaseFilterBackend
from apps.order.models import OrderGoods

class UserCenterFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(user=request.user_obj)
        return queryset