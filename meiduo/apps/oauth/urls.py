# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author:xiaoheng
# @time: 18-8-23 下午7:43


from django.conf.urls import url
from . import views

urlpatterns = [
    #   /oauth/qq/statues/
    url(r'^qq/statues/$',views.QQAuthURLView.as_view(),name='statues'),
    url(r'^qq/users/$',views.QQTokenView.as_view()), #

]