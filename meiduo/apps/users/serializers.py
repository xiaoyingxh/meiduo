# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author:xiaoheng
# @time: 18-8-21 下午4:26
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection


class RegisterUserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(label='确认密码',allow_null=False,allow_blank=False,write_only=True)
    # sms_code = serializers.CharField(label='短信验证',max_length=6,min_length=6,allow_null=False,allow_blank=False,write_only=True)
    # allow = serializers.CharField(label='是否同意协议',allow_null=False,allow_blank=False,write_only=True)

    password2 = serializers.CharField(label='校验密码', allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, allow_null=False, allow_blank=False,
                                     write_only=True)
    allow = serializers.CharField(label='是否同意协议', allow_null=False, allow_blank=False, write_only=True)

    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段


    class Meta:
        model = User
        fields = ('id','username','password','mobile','password2','sms_code','allow','token')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 单字段 手机号码校验  value是传递过来的值
    def validate_mobile(self, value):

        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号码格式输入有误')

        return value

    # 多单字段校验协议是否同意
    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('未同意协议内容')

        return value

    # 密码校验多个字段校验

    def validate(self, attrs):
        # 比较密码
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # 判断密码是否一样
        if password != password2:
            raise serializers.ValidationError('密码输入不一致')
        # 获取用户提交的验证码
        code = attrs.get('sms_code')
        # 获取rsdis的验证
        radis_conn = get_redis_connection('code')
        # 获取手机号码
        mobile = attrs.get('mobile')
        radis_code = radis_conn.get('sms_%s' % mobile)
        # 判断验证码有没有鬼泣
        if radis_code is None:
            raise serializers.ValidationError('验证码过期')
        # 判断验证阿妈是否正确
        if radis_code.decode() != code:
            raise serializers.ValidationError('验证码不正确')

        return attrs


        #
        # """
        # 父类不满足,我们需要重写
        # 因为validate有6个字段
        # 我们实际入库3个
        # 需要删除其他3个
        #
        # """

    def create(self, validated_data):

        del validated_data['sms_code']
        del validated_data['allow']
        del validated_data['password2']
        user = super().create(validated_data)


        #密码转成看不见状态
        user.set_password(validated_data['password'])
        #保存数据
        user.save()

        from rest_framework_jwt.settings import api_settings
        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token


        return user

class  UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')



class EmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """

    class Meta:
        model = User
        fields = ('id','email')
        extra_kwargs = {
            'email':{
                'required':True
            }
        }

    from django.core.mail import send_mail
    def update(self, instance, validated_data):

        email = validated_data['email']
        instance.email = email
        instance.save()

        # subject = '美多主题'
        # message= ''
        #
        # from_email = settings.EMATL_FROM
        # recipient_list = [email]
        #
        #
        # # url = instance.generic_verify_url()
        #
        #
        # html_message = '<p>尊敬的用户您好！</p>' \
        #            '<p>感谢您使用美多商城。</p>' \
        #            '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
        #            '<p><a href="%s">%s<a></p>' % (email, url, url)
        # send_mail(subject,message,from_email,recipient_list,html_message=html_message)

        url = instance.generic_verify_url()
        from celery_tasks.email.tasks import send_verify_mail

        send_verify_mail.delay(email,url)



        return instance



