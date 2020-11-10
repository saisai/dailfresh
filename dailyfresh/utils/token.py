import os,sys
sys.path.append("/Users/songyi/PycharmProjects/dailyfresh/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")

from itsdangerous import  TimedJSONWebSignatureSerializer as Sign
from django.conf import settings
from itsdangerous import SignatureExpired


class Token(object):
    serializer = Sign(settings.SECRET_KEY, 3000)
    __first = None

    def __new__(cls, *args, **kwargs):
        "使用单例模式创造加解密对象"
        if not Token.__first:
            Token.__first = object.__new__(cls)
        return Token.__first

    def encryt(self,text):
        info = {"key":text}
        res = self.serializer.dumps(info)
        return res

    def decryt(self,params):
        try:
            res = self.serializer.loads(params)
            return res
        except SignatureExpired as e:
            "超时处理"
            return
