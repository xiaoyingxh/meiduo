# -*- coding: utf-8 -*-
# @File  : pagination.py
# @Author:xiaoheng
# @time: 18-8-31 下午7:23

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20