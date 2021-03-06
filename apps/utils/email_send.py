# _*_ coding:utf-8 _*_
__author__ = "devin"
__date__ = "2018/4/10 19:48"
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from djangoCourse.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length =len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "在线注册激活链接"
        email_body = "请点击链接激活账号：http://127.0.0.1:8050/user/activate/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print send_status
        return send_status
    elif send_type == "forget":
        email_title = "密码重置链接"
        email_body = "请点击链接修改密码：http://127.0.0.1:8050/user/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status
