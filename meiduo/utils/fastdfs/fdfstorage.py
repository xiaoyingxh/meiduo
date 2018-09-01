# -*- coding: utf-8 -*-
# @File  : fdfstorage.py
# @Author:xiaoheng
# @time: 18-8-30 上午10:17

from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.utils.deconstruct import deconstructible



@deconstructible
class MyStorage(Storage):
    # def __init__(self, option=None):
    #     if not option:
    #         option = settings.CUSTOM_STORAGE_OPTIONS


    def __init__(self, conf_path=None, ip=None):
        if conf_path is None:
            conf_path = settings.FDFS_CLIENT_CONF
        self.conf_path = conf_path

        if ip is None:
            ip = settings.FDFS_URL
        self.ip = ip




    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):

        #创建client对象
        client = Fdfs_client('utils/fastdfs/client.conf')
        #获取文件
        file_data = content.read()
        #上传
        result = client.upload_by_buffer(file_data)
        #判断上传结果
        if result.get('Status') == 'Upload successed.':
            #返回上传的字符串
            return result.get('Remote file_id')
        else:
            raise Exception('上传失败')


    def exists(self, name):
        # 判断文件是否存在，FastDFS可以自行解决文件的重名问题
        # 所以此处返回False，告诉Django上传的都是新文件
        return False

    def url(self, name):
        #返回文件的完整URL路径
        return "http://192.168.229.133:8888/" + name




