"""
-------------------------------------------------
    File Name:   c_pagination.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/16 9:57
-------------------------------------------------
    Change Activity:
          2023/3/16 9:57
-------------------------------------------------
"""

import contextlib
from collections import OrderedDict

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import _positive_int

from utils.c_restframework.c_response import JsonResponse


class PaginationException(APIException):
    """
    页码超出范围问题
    """
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = '页码超出范围'
    default_code = '页码超出范围'


class MyPageNumberPagination(PageNumberPagination):
    page = 1
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "size"
    # 最大页数不超过50
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            page_size = self.page_size

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
            if paginator.num_pages > 1 and self.template is not None:
                self.display_page_controls = True
            self.request = request

            return list(self.page)
        except Exception:
            raise PaginationException

    def get_page_size(self, request):
        if self.page_size_query_param:
            with contextlib.suppress(KeyError, ValueError):
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
        return self.page_size

    def get_paginated_response(self, data):
        """
        自定义分页显示
        :param data:返回的数据
        :return:
        """
        return JsonResponse(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
