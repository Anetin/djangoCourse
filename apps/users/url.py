# _*_ coding:utf-8 _*_

__author__ = "devin"
__date__ = "2018/5/30 10:08"

from django.conf.urls import patterns, url
from users.views import *

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/(?P<active_code>.*)/$', ResetPwdView.as_view(), name='reset'),
    url(r'^avatar/$', UploadAvatarView.as_view(), name='uploadAvatar'),
    url(r'^getUserInfo/$', GetUserInfo.as_view(), name='getUserInfo'),
    url(r'^getCaptcha/$', GetCaptcha.as_view(), name='getCaptcha'),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='updatePwd'),
    url(r'^activate/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='activeUser'),
)


