from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from django_redis import get_redis_connection
from django.http import HttpResponse
from .serializers import RegisterSMSCodeSerializer
from libs.captcha.captcha import captcha
from . import constants
from libs.yuntongxun.sms import CCP

class RegisterImageCodeView(APIView):
    """
    1.生成验证码:
    GET:   verifications/imagecodes/(?P<image_code_id>.+)/
    需要通过js生成唯一一个验证码,以确保后台对图片进行校验

    通过第三方库,生成图片和验证码 需啊呀怕对验证码进行redis保存
    1.创建图片和验证码
    2.通过redis进行保存验证码 需要在设置中添加 验证码数据库选项
    3.把图片返回

    """

    def get(self, request, image_code_id):
        # 1.创建图片和验证码
        text, image = captcha.generate_captcha()
        # 2.通过redis进行保存验证码  60秒就过期
        redis_conn = get_redis_connection('code')     #就是60秒的意思
        redis_conn.setex('img_%s' % image_code_id,constants.IMAGE_GOOD_EXPIRE , text)
        # 3.把图片返回

        return HttpResponse(image, content_type='image/jpeg')



class RegisterSMSCodeView(APIView):

    """
    1.获取短信验证码:
    GET:verifications/smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx&image_c
    获取端在新验证码  先检验

    思路:
    创建序列化器.定义text和image_code_id
    redis判断该用户是否频繁获取
    生成该用户的短信验证码
    redis增加记录
    发送短信
    返回响应

    """
    serializer_class = RegisterSMSCodeSerializer


    def get(self,request,mobile):

        data = request.query_params
        serializer = RegisterSMSCodeSerializer(data = data)

        serializer.is_valid()


        #生成短信
        from random import randint
        sms_code = '%06d'%randint(0,999999)
        #redis记录短信内容
        redis_conn = get_redis_connection('code')
        # 判断该用户是否频繁获取
        if redis_conn.get('sms_flag_%s' % mobile):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        #记录为string类型
        redis_conn.setex('sms_%s'%mobile,5*60,sms_code)
        redis_conn.setex('sms_flag_%s' % mobile, 60, 1)
        #发送短信
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, 5], 1)
        # 返回响应

        #异步任务  delay调用
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code)


        return Response({'message': 'ok'})



