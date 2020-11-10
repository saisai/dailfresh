from rest_framework.generics import CreateAPIView, ListCreateAPIView,ListAPIView
from rest_framework.views import APIView
from apps.user import models
#序列器类
from apps.user.serializer.serializer_class import UserSerializers,\
                                                  AddressGetSerializer,AddressPostSerializer,\
                                                  UserCenter_infoSerializer
#过滤器
from apps.user.filter.filter_bankend import AddressFilter
from django.conf import settings
from celery_tasks.tasks import send_QQmail
from utils.token import Token

from rest_framework.response import Response

#model对象转字典
from django.forms.models import model_to_dict

from django_redis import get_redis_connection


class RegisterView(CreateAPIView):
    """
    注册
    1.验证是否为空/是否重复/邮箱格式
    2.发送邮件
    3.激活
    """
    serializer_class = UserSerializers
    queryset = models.User.objects

    def perform_create(self, serializer):
        "保存数据前，额外需要传递的参数"
        obj = serializer.save(is_staff=0, is_active=0)

        # 生成激活码
        tk_obj = Token()
        token = tk_obj.encryt(obj.id).decode("utf-8")

        reciver = obj.email
        content = settings.CONTENT.format(obj.username, token, token)
        # celery发送邮件
        send_QQmail.delay(
            settings.SUBJECT,
            '',
            settings.SENDER,
            reciver,
            content
        )


class LoginView(APIView):
    """
    用户登录

    """
    def verify_account(self,request):
        username = request.data["username"]
        password = request.data["password"]
        obj = models.User.objects.filter(username=username,password=password).first()
        return obj

    def create_session(self,user,request):
        request.session.flush()
        #将用户信息存入session
        # request.session["user_info"] = pickle.dumps(model_to_dict(user,exclude=[""]))
        request.session["user"] = user
        #用户订单信息

    def set_cookie(self,request,user):
        res = {
            "code": "",
            "userinfo": {
                "username": user.username
            },
            "redirect_url": ""
        }
        response = Response(res)
        remember = request.data["remember"]
        if not int(remember):
            response.delete_cookie("username")
            return response
        response.set_cookie("username", user.username, max_age=24 * 3600)
        return response

    def post(self,request):
        if not request.user_obj:
            user = self.verify_account(request)
            if not user:
                return Response({
                    "code":"",
                    "error": "登录失败",
                    "redirect_url": ""})
        else:
            user = request.user_obj

        self.create_session(user,request)

        return self.set_cookie(request,user)


class LogoutView(APIView):
    """
    注销
    todo 还需要删除浏览记录
    """
    def get(self,request):

        request.session.flush()

        return Response({
            "code":302,
            "url":"index.html"
        })



class ActiveView(APIView):
    "用户激活"
    # serializer_class = ActiveSerializer
    # queryset = models.User

    def get_id(self, request):

        "解密获取用户id"

        token = request.query_params.get("token")
        obj = Token()
        result = obj.decryt(token)

        if result: return result

    def patch(self, request, *args, **kwargs):
        id = self.get_id(request)
        if not id:
            return Response({
                "msg": "链接已超时",
                "url": "跳转的链接"
            })

        obj = models.User.objects.filter(pk=id["key"]).first()
        if obj.is_active:
            return Response({"msg":"您已激活!"})

        obj.is_active = 1
        obj.save()

        res = {
            "user":{
                "用户名":obj.username,
                "状态":obj.is_active
            },
            "redirect_url":""
        }

        return Response(res)


class UserInfoView(ListAPIView):
    "用户信息页面/address存放用户收件信息"

    queryset = models.Address.objects
    filter_backends = [AddressFilter,]
    serializer_class = UserCenter_infoSerializer

class UserOrderView(APIView):
    "用户订单"
    pass

class AddressView(ListCreateAPIView):
    """
    用户中心
    todo 设置默认地址还未做
    """
    queryset = models.Address.objects
    filter_backends = [AddressFilter,]

    def get_default(self):
        if not models.Address.objects.filter(user=self.request.user_obj,is_default=True):
            default = True
        else:default = False
        return default

    def get_serializer_class(self):
        if self.request._request.method == "GET":
            return AddressGetSerializer
        return AddressPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user_obj,is_default=self.get_default())


class UserHistoryView(APIView):
    """
    添加用户浏览历史记录
    传递格式:
            goods_id: ,

    session解析当前用户
    """
    def get(self,request):
        goods_id = request.query_params.get("goods_id")
        conn = get_redis_connection("default")

        key = "history_{}".format(request.user_obj.id)
        #redis查询是否存在该key
        exists = conn.lrange(key,0,-1)

        if exists and goods_id.encode("utf-8") in exists:
            conn.lrem(key, 0, goods_id)
        conn.lpush(key,goods_id)
        conn.ltrim(key,0,4)

        dic = {
            "user":request.user_obj.id,
            "history":conn.lrange(key,0,-1)
        }
        return Response(dic)


