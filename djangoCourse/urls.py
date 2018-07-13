"""djangoCourse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
# from django.conf.urls import url
# from django.contrib import admin

import users.url
from djangoCourse import settings

from message.views import getform
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^form/$', getform, name='go_form'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'^user/', include(users.url)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
