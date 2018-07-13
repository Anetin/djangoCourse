# _*_ coding:utf-8 _*_
import json
import traceback

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import UserProfile, EmailVerifyRecord
from .form import LoginForm,RegisterForm, ForgetForm, UploadImageForm, ModifyPwdForm
from utils.email_send import send_register_email

from my_tools.tools import getResultCode, my_model_to_dict


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username = username) | Q(email = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        errs = login_form.errors.items
        for key,err in errs:
            print(key,err)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return getResultCode([], 1, u"登录成功！", 1)
                else:
                    return getResultCode([],0,u"用户未激活！",4)
            else:
                return getResultCode([],0,u"用户名或密码错误！",4)
        else:
            return getResultCode([], 0, u"用户名或密码格式不正确！", 4)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


class RegisterView(View):
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user_profile = UserProfile.objects.filter(username=username)
            if user_profile.exists():
                return getResultCode([], 0, u"注册失败！该用户已注册", 4)
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            send_email_status = send_register_email(username, "register")
            if(send_email_status):
                return getResultCode([], 1, u"注册成功，请登录邮箱激活用户！", 1)
            else:
                return getResultCode([], 1, u"注册成功，但发送邮箱失败，请联系管理员！", 1)
        else:
            print(register_form.errors)
            if(register_form.errors['captcha']):
                captcha_err_str = register_form.errors['captcha'][0]
                return getResultCode([], 0, captcha_err_str, 4)
            if (register_form.errors['email']):
                email_err_str = register_form.errors['email'][0]
                return getResultCode([], 0, email_err_str, 4)
            if (register_form.errors['password']):
                password_err_str = register_form.errors['password'][0]
                return getResultCode([], 0, password_err_str, 4)



class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        # return getResultCode([], 1, u"激活成功！", 1)
        return HttpResponseRedirect("/user/login/")


class LogoutView(View):
    def post(self, request):
        if request.user.is_authenticated():
            print("用户已登陆")
        else:
            print("用户未登陆")
        logout(request)
        return getResultCode([], 1, u"注销成功！", 1)

    # @method_decorator(login_required(login_url="/login/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(LogoutView, self).dispatch(*args, **kwargs)


from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
class GetCaptcha(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        data = {}
        data['hashkey'] = hashkey
        data['imgage_url'] = imgage_url
        return getResultCode(data, 1, u"成功！", 1)


class ForgetPwdView(View):
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        email = ""
        if forget_form.is_valid():
            email = request.POST.get("email", "")
        send_email_status = send_register_email(email, "forget")
        if (send_email_status):
            return getResultCode([], 1, u"链接已发送到邮箱，请登录邮箱修改密码！", 1)

class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        # return getResultCode([], 1, u"激活成功！", 1)
        return HttpResponseRedirect("/user/login/")


class GetUserInfo(View):
    def post(self, request):
        username = request.FILES.get("username", "admin")
        json_dict = {}
        # data = {}
        # data["list"] = []
        try:
            qry = UserProfile.objects.filter(username=username)
            fields = ['username', 'email', 'is_superuser', 'is_actice', 'is_staff', 'nick_name', 'birday', 'gender', 'address', 'mobile', 'image', ]
            if qry.exists():
                json_dict = my_model_to_dict(qry[0], fields=fields)
                json_dict["image"] = str(json_dict["image"])
            # data["list"].append(json_dict)
        except Exception, e:
            transaction.rollback()
            traceback.print_exc()
            return getResultCode([], 0, '失败!' + e.message, 4)
        return getResultCode(json_dict)

class UploadAvatarView(View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            image_form.save()
            return getResultCode([])
            # request.user.image = image
            # request.user.save()
        # avatar = request.FILES.get("image", "")
        # userId = request.POST.get("userId", "")
        else:
            return getResultCode([], 0, '失败!', 4)


class UpdatePwdView(View):
    '''登录状态下修改密码，个人中心'''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return getResultCode([], 0, '密码不一致!', 4)
            user = request.user
            if user.is_anonymous():
                return getResultCode([], 0, '失败,请先登录!', 4)
            user.password = make_password(password2)
            user.save()
            return getResultCode([], 1, '修改成功，请重新登录!', 1)
        else:
            return getResultCode(modify_form.errors, 0, '失败!', 4)

