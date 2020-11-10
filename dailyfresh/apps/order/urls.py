from django.conf.urls import url
from apps.order.views import OrderIndexView,CreateOrderView,UserCenterOrder,OrderPayView,CheckPayView

urlpatterns = [
    #订单首页
    url(r'^order_index',OrderIndexView.as_view()),
    #创建订单
    url(r'^create_order',CreateOrderView.as_view()),
    #用户中心订单
    url(r'^user_center_order',UserCenterOrder.as_view()),
    #Alipay支付
    url(r'^pay',OrderPayView.as_view()),
    #检测订单是否支付成功
    url(r'^check',CheckPayView.as_view()),
]
