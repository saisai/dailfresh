from celery import Celery
from django.core.mail import send_mail
import os,sys

sys.path.append("/Users/songyi/PycharmProjects/dailyfresh/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
app = Celery('tasks',broker='redis://192.168.1.6:6379/8')


@app.task
def send_QQmail(subject,msg,sender,reciver,content):
    try:
        send_mail(
            subject = subject,
            message = msg,
            from_email = sender,
            recipient_list = [reciver],
            html_message = content,
            fail_silently = True
        )
    except Exception as e:
        pass


