# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author:xiaoheng
# @time: 18-8-28 下午5:37

from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from .views import AreasInfoView

router = DefaultRouter()
router.register(r'infos',AreasInfoView,base_name='area')

urlpatterns = [
    # url(r'^',include(router.urls))
]

#添加省市区信息查询路由
urlpatterns += router.urls