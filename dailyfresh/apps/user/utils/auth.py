from rest_framework import authentication
from rest_framework import exceptions
from apps.user import models

class LoginAuthenticate(authentication.BaseAuthentication):
    def is_active(self,obj):
        if not obj.is_active:
            raise exceptions.AuthenticationFailed("未激活!")

    def authenticate(self, request):
        username = request.data["username"]
        pwd = request.data["password"]

        user = models.User.objects.filter(username=username,password=pwd).first()
        if not user:
            raise exceptions.AuthenticationFailed("用户名or密码错误")

        self.is_active(user)

        return (user,None)