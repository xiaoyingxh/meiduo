# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author:xiaoheng
# @time: 18-8-30 下午4:50

from django.conf.urls import url
from . import views

urlpatterns = [
    #/goods/categories/
    url(r'^home/$',views.HomeView.as_view(),name='HomeView'),

    # url(r'^categories/$',views.CategoryView.as_view(),name='cagegories'),
    #/goods/categories/(?P<category_id>\d+)/hotskus/
    url(r'^categories/(?P<category_id>\d+)/hotskus/$',views.HotSKUView.as_view()),

    url(r'^categories/(?P<category_id>\d+)/skus/$',views.SKUListView.as_view()),

]