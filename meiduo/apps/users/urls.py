# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author:xiaoheng
# @time: 18-8-19 下午8:43


from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    #/users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view(),name='usernamecount'),
    #/users/phones/(?P<mobile>1[345789]\d{9})/count/
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$',views.RegisterPhoneCountAPIView.as_view(),name='phonecount'),

    # users/
    url(r'^$', views.RegisterUserView.as_view()),

    # users/auths/
    url(r'^auths/$', obtain_jwt_token),

    url(r'^infos/$',views.UserInfoView.as_view()),

    url(r'^emails/$', views.EmailView.as_view(), name='send_mail'),

    url(r'^list/$',views.UserListView.as_view()),
#
    url(r'^email/verification/$',views.EmailActiveView.as_view()),

    url(r'^browerhistories/$', views.UserHistoryView.as_view(), name='history'),





]