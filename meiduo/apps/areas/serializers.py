# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author:xiaoheng
# @time: 18-8-28 下午5:37

from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """
    class Meta:
        model = Area
        fields = ('id', 'name','parent_id')


class SubAreaSerializer(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    """
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')