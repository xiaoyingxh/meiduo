# -*- coding: utf-8 -*-
# @File  : utlis.py
# @Author:xiaoheng
# @time: 18-8-23 下午9:24
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

import json

from meiduo import settings


class OauthQQTllo(object):

    def get_auth_url(self):

        base_url = 'https://graph.qq.com/oauth2.0/authorize?'

        # 组织参数
        params = {
            'response_type': 'code',
            'client_id': settings.QQ_APP_ID,
            'redirect_uri': settings.QQ_REDIRECT_URL,
            'state': 'test',
        }

        # 对参数进行urlencode,然后拼接url
        auth_url = base_url + urlencode(params)

        return auth_url

    def get_access_tokrn_by_code(self,code):

        base_url = 'https://graph.qq.com/oauth2.0/token?'


        params = {
            'grant_type': 'authorization_code',
            'client_id': settings.QQ_APP_ID,
            'client_secret': settings.QQ_APP_KEY,
            'code': code,
            'redirect_uri': settings.QQ_REDIRECT_URL
        }

        # 对参数进行urlencode,然后拼接url
        url = base_url + urlencode(params)

        response = urlopen(url)

        data = response.read().decode()

        access_data = parse_qs(data)

        token = access_data.get('access_token'[0])

        return token

    def get_openid_by_token(self, token):
        """
        PC网站：https://graph.qq.com/oauth2.0/me
        2 请求方法
        GET
        3 请求参数
        请求参数请包含如下内容：
        参数	是否必须	含义
        """

        # 1. base_url
        base_url = 'https://graph.qq.com/oauth2.0/me?'
        # 2. 参数
        params = {
            'access_token':token
        }
        # 3. url
        url = base_url + urlencode(params)
        # 4. 根据url获取数据
        response = urlopen(url)

        data = response.read().decode()

        # print(data)
        # 5. 解析数据
        # 因为它返回的数据 不是 字典类型,我们要想获取 字典数据,需要对这个字符串进行截取
        #'callback( {"client_id":"101474184","openid":"483C55DADEF65CC5735695CBC262F979"} );'
        try:
            openid_data = json.loads(data[10:-4])
        except Exception:
            raise Exception('数据获取错误')


        return openid_data['openid']
