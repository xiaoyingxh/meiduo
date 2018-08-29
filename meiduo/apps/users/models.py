from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from itsdangerous import BadData
from rest_framework.serializers import Serializer


class User(AbstractUser):

    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号")

    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generic_verify_url(self):

        serializer = Serializer(settings.SECRET_KEY, 3600)

        # 加载用户信息
        token = serializer.dumps({'user_id': self.id, 'email': self.email})
        # 注意拼接的过程中对 token进行decode操作
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token.decode()

        return verify_url


    @staticmethod
    def generic_user_info(self,token):

        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            result = serializer.loads(token)
        except BadData:
            return None
        else:
            id = result.get('id')
            email = result.gte('email')

            try:
                user = User.objects.grt(id=id,email=email)
            except User.DoesNotExist:
                 return None
            else:
                return user


from utils.models import BaseModel

class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']