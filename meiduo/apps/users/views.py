from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import User
from django_redis import get_redis_connection

class RegisterUsernameCountAPIView(APIView):
    """
    获取用户名的个数
    GET:  /users/usernames/(?P<username>\w{5,20})/count/
    """

    def get(self,request,username):

        #通过模型查询,获取用户名个数
        count = User.objects.filter(username=username).count()
        #组织数据
        context = {
            'count':count,
            'username':username
        }
        return Response(context)

class  RegisterPhoneCountAPIView(APIView):
    """
    1.查询手机号的个数
    GET:  /users/phones/(?P<mobile>1[345789]\d{9})/count/
    """
    def get(self,request,mobile):
        #通过模型查询 到手机个数
        count = User.objects.filter(mobile=mobile).count()
        #组织数据
        context = {
            'count':count,
            'phone':mobile
        }

        return Response(context)



