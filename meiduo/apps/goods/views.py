from django.db.migrations import serializer
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from goods.models import GoodsCategory, GoodsChannel, SKU
from contents.models import ContentCategory
from collections import OrderedDict


# Create your views here.
from goods.serializers import SKUSerializer


class HomeView(View):
    """
    获取首页分类数据

    GET /goods/categories/
    """

    def get(self, request):
        # categories = {
        #     1: { # 组1
        #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
        #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
        #     },
        #     2: { # 组2
        #
        #     }
        # }
        # 初始化存储容器
        categories = OrderedDict()
        # 获取一级分类
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')

        # 对一级分类进行遍历
        for channel in channels:
            # 获取group_id
            group_id = channel.group_id
            # 判断group_id 是否在存储容器,如果不在就初始化
            if group_id not in categories:
                categories[group_id] = {
                    'channels': [],
                    'sub_cats': []
                }

            one = channel.category
            # 为channels填充数据
            categories[group_id]['channels'].append({
                'id': one.id,
                'name': one.name,
                'url': channel.url
            })
            # 为sub_cats填充数据
            for two in one.goodscategory_set.all():
                # 初始化 容器
                two.sub_cats = []
                # 遍历获取
                for three in two.goodscategory_set.all():
                    two.sub_cats.append(three)

                # 组织数据
                categories[group_id]['sub_cats'].append(two)

        contents = {}
        content_categories = ContentCategory.objects.all()
        # content_categories = [{'name':xx , 'key': 'index_new'}, {}, {}]

        # {
        #    'index_new': [] ,
        #    'index_lbt': []
        # }
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context)
        # return HttpResponse({'message' : "00000"})




class HotSKUView(GenericAPIView):
    """
    获取热销商品
    GET /goods/categories/(?P<category_id>\d+)/hotskus/
    # """
    serializer_class = SKUSerializer
    pagination_class = None

    def get_queryset(self):

        category_id = self.kwargs['category_id']

        return SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]
    # def get(self,request,category_id):
    #
    #     skus = SKU.objects.filter(category_id = category_id,is_launched=True).order_by('-sales')
    #
    #     serializer = SKUSerializer(instance=skus,many=True)
    #
    #     return Response(serializer.data)



class SKUListView(ListAPIView):
    """
    商品列表数据
    GET /goods/categories/(?P<category_id>\d+)/skus/?page=xxx&page_size=xxx&ordering=xxx
    """

    serializer_class = SKUSerializer
    # 通过定义过滤后端 ，来实行排序行为
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_time', 'price', 'sales')


    def get_queryset(self):
        categroy_id = self.kwargs.get("category_id")
        return SKU.objects.filter(category_id=categroy_id, is_launched=True)