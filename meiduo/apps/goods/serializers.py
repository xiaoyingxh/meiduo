# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author:xiaoheng
# @time: 18-8-31 下午4:06
from rest_framework import serializers

from goods.models import SKU


class SKUSerializer(serializers.ModelSerializer):



    class Meta:
        model = SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')