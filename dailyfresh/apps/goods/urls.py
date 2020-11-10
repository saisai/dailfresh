from django.conf.urls import url
from apps.goods.views import GetIndexDataView,GetGoodsListView,GetGoodsView

urlpatterns = [
    #首页info
    url(r'^goods_index/',GetIndexDataView.as_view()),
    #分类商品页
    url(r'^goods_list/',GetGoodsListView.as_view()),
    #商品详情
    url(r'^goods/',GetGoodsView.as_view()),
    #
]
