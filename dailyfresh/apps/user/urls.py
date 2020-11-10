from django.conf.urls import url
from apps.user.views import RegisterView,LoginView,ActiveView,LogoutView,UserInfoView,UserOrderView,AddressView,UserHistoryView

urlpatterns = [
    #用户注册
    url(r'^register',RegisterView.as_view()),
    #用户登录
    url(r'^login',LoginView.as_view()),
    #用户登出
    url(r'^logout',LogoutView.as_view()),
    # 用户激活
    url(r'^active',ActiveView.as_view()),
    # 用户中心-信息页
    url(r'^user_center', UserInfoView.as_view()),
    # 用户中心-订单页
    url(r'^order', UserOrderView.as_view()),
    # 用户中心-地址页
    url(r'^address', AddressView.as_view()),
    # 添加用户历史记录
    url(r'^add_his', UserHistoryView.as_view()),

]
