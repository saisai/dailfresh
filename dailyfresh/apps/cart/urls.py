
from django.conf.urls import url
from apps.cart.views import AddGoodsView,CartView,Update_CartView,Del_cartView


urlpatterns = [
    url(r'^add_goods', AddGoodsView.as_view()), #添加商品到购物车接口
    url(r'^cart_list', CartView.as_view()), #购物车页面数据接口
    url(r'^update_cart', Update_CartView.as_view()), #更新购物车商品数量
    url(r'^del_cart', Del_cartView.as_view()) #更新购物车商品数量
]
