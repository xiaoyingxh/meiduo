# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author:xiaoheng
# @time: 18-8-20 下午5:32

from rest_framework import serializers
from django_redis import get_redis_connection
from redis.exceptions import RedisError
import logging
from rest_framework.serializers import Serializer


logger = logging.getLogger('meiduo')

class RegisterSMSCodeSerializer(serializers.Serializer):
    #校验 验证码和image
    text = serializers.CharField(label='图片的验证码',max_length=4,min_length=4,required=True)
    image_code_id = serializers.UUIDField(label='验证码的唯一性uuid')

    #需要在validate中进行判断
    #序列化器进行验证的4种方法
    #1.字段类型 UUIDField
    #2.字段选项 max_length
    #3.单个字段校验 def validate_字段名
    #4.多个字段名 def validate

    def validate(self, data):
        #1.获取用户提交
        text = data.get('text')
        image_code_id = data.get('image_code_id')

        #2.获取redis中的数据
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('img_%s'%image_code_id)
        #判断获取的redis_text的值

        if redis_text is None:
            raise serializers.ValidationError('图片验证码已过期')

        try:
            redis_conn.delete('img_%s'%image_code_id)
        except RedisError as e:
            logging.error(e)

        #3.比较 redis是bystes类型  不区分大小写
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('图片验证码输入错误')


        return data


