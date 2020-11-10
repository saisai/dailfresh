#!/usr/bin/env python
# -*- coding:utf-8 -*-

from alipay import AliPay


class AliPayObj(AliPay):
    _first = None

    def __new__(cls, *args, **kwargs):
        if not cls._first:
            cls._first = super().__new__(cls)
        return cls._first


