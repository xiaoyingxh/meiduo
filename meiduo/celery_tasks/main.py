# -*- coding: utf-8 -*-
# @File  : main.py
# @Author:xiaoheng
# @time: 18-8-21 下午3:30
"""
1.我们需要告知celey我们当前的django配置文件在哪里
2.创建celey实例对象
3.让celey实例对象 加载配置信息实现broker的设置
4.让celey实例对象自动检测任务

"""
from celery import Celery

#为celey使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo.settings'

#创建Celery对象
#参数main 设置脚本名
app = Celery('celery_tasks')

#加载配置文件
app.config_from_object('celery_tasks.config')

#自动加载任务
app.autodiscover_tasks(['celery_tasks.sms'])