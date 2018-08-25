# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author:xiaoheng
# @time: 18-8-21 下午3:14
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app


@app.task(name='aaaaa')
def send_sms_code(mobile,sms_code):
    #任务发送短信
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, 5], 1)