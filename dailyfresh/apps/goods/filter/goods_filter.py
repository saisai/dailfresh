#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.filters import BaseFilterBackend

class GoodsTypeFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
        sort:
            1.id
            2.price
            3.sale
        """
        sort = request.query_params.get('sort')
        type_id = request.query_params.get("type_id")
        if sort!="id":
            sort = "-{}".format(sort)
        query = queryset.filter(type_id=type_id).order_by(sort)
        return query