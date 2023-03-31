"""
-------------------------------------------------
    File Name:   c_exception.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/22 11:13
-------------------------------------------------
    Change Activity:
          2023/3/22 11:13
-------------------------------------------------
"""

from utils.c_restframework.c_validator import CustomUniqueValidator, CustomValidationError
from rest_framework.views import exception_handler
from utils.c_restframework.c_response import JsonResponse
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):

    message = '服务器错误'

    response = exception_handler(exc, context)
    # 自定义异常抛出错误！
    if isinstance(exc, (CustomValidationError, CustomUniqueValidator, ValidationError)):
        message = exc.detail if isinstance(response.data, dict) else '字段校验错误'
        return JsonResponse(msg=message, code=response.status_code)

    if response is not None:
        if response.status_code == 404:
            try:
                message = exc.detail
            except KeyError:
                message = "未找到"

        if response.status_code == 400:
            message = '输入错误'

        elif response.status_code == 401:
            try:
                message = exc.default_detail
            except Exception:
                message = "认证失败或者Token失效"

        elif response.status_code == 403:
            message = "没有相应的权限"

        elif response.status_code == 405:
            message = '错误的请求方法'

        elif response.status_code >= 500:
            message = "服务器错误"
    return JsonResponse(msg=message, code=response.status_code)
