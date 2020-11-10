from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.conf import settings

class SessionCheckMiddleware(MiddlewareMixin):
    """校验session"""

    def process_view(self, request, view_func, view_args, view_kwargs):
        """检测session"""
        view_name = '.'.join((view_func.__module__, view_func.__name__))
        print(view_name)
        exclusion_set = getattr(settings, 'EXCLUDE_FROM_MY_MIDDLEWARE', set())
        if view_name in exclusion_set:
            #首页是白名单,需要检测用户是否登录
            return None

        session_id = request.COOKIES.get("sessionid")
        # redis中获取session进行匹配
        if not session_id or not request.session.exists(session_id):
            if view_name != "apps.user.views.LoginView":
                #需要跳转到login
                # return HttpResponseRedirect("login")
                return HttpResponse("请重新登录")
            request.user_obj = None
        else:
            #session中取出用户信息存到request对象中
            request.user_obj = request.session.get("user")
            #订单信息
            #浏览记录
            #购物车
            # ...
