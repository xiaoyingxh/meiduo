from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from goods.models import SKU
from goods.serializers import SKUSerializer
from .serializers import  UserHistorySerializer
from .models import User
from django_redis import get_redis_connection
from .serializers import RegisterUserSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from .serializers import UserInfoSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from .serializers import EmailSerializer

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



class RegisterUserView(APIView):
    """
    用户注册
    POST /users/

    用户注册我们需要对数据进行校验,同时需要数据入库
    """

    def post(self,request):
        serialiazer = RegisterUserSerializer(data=request.data)
        #进行校验
        serialiazer.is_valid()
        #保存数据
        serialiazer.save()

        return  Response({'message':'ok'})



# class UserInfoView(GenericAPIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#
#         user = request.user
#
#         serializer = UserInfoSerializer(instance=user)
#
#         return Response(serializer.data)


class UserInfoView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user



class EmailView(UpdateAPIView):
    """
    保存邮箱
    PUT /users/emails/
    """

    permission_classes = [IsAuthenticated]

    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user



class UserListView(GenericAPIView):

    serializer_class = UserInfoSerializer

    queryset = User.objects.all()

    def get(self,request):

        #1.查询所有数据
        books = self.get_queryset()

        #2.创建序列化器,用序列化器实现将模型转为字典
        serializer = self.get_serializer(books,many=True)

        #3.返回数据
        return Response(serializer.data)


class EmailActiveView(APIView):

    def get(self,request):

        token = request.query_params.grt('token')

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.generic_user_info(token)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()

        return  Response({'message':'ok'})



class UserHistoryView(mixins.CreateModelMixin, GenericAPIView):
    """
    用户浏览历史记录
    POST /users/histories/
    GET  /users/histories/
    数据只需要保存到redis中
    """


    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.get_serializer(data = request.data)

        serializer.is_valis()

        serializer.save()

        """
        保存
        """
        return Response(serializer.data)


    """
      用户浏览历史记录
      POST /users/browerhistories/
      GET  /users/browerhistories/
      数据只需要保存到redis中
      """
    def get(self, request):
        """获取"""
        # 获取用户信息
        user_id = request.user.id
        # 连接redis
        redis_conn = get_redis_connection('history')
        # 获取数据
        history_sku_ids = redis_conn.lrange('history_%s' % user_id, 0, 5)
        skus = []
        for sku_id in history_sku_ids:
            sku = SKU.objects.get(pk=sku_id)
            skus.append(sku)
        # 序列化
        serializer = SKUSerializer(skus, many=True)

        return Response(serializer.data)


