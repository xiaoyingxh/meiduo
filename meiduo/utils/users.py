# -*- coding: utf-8 -*-
# @File  : users.py
# @Author:xiaoheng
# @time: 18-8-22 下午9:25
from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

"""
修改Django认证系统的认证后端需要继承django.contrib.auth.backends.ModelBackend，并重写authenticate方法。
根据username参数查找用户User对象，username参数可能是用户名，也可能是手机号

若查找到User对象，调用User对象的check_password方法检查密码是否正确

"""
import re
from django.contrib.auth.backends import ModelBackend
def get_user_by_account(account):
    #根据用户输入的username来判断手机号是否是用户名
    try:
        if re.match(r'1[3-9]\d{9}',account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)

    except User.DoesNotExist:
        user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):
    """
        自定义用户名或手机号认证
        """

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = get_user_by_account(username)

        if user is not None and user.check_password(password):

            return user


















