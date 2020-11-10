import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
import django
django.setup()
from apps.goods import models
from django_redis import get_redis_connection
import json
from django.conf import settings

from apps.order.models import OrderInfo



dir = os.path.join(settings.BASE_DIR, 'apps/order/')
app_private_key_string = open(dir+'app_private_key.pem').read()
alipay_public_key_string = open(dir+'alipay_public_key.pem').read()


print(app_private_key_string )
