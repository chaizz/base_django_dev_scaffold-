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

from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from utils.c_restframework.c_response import JsonResponse
from utils.c_restframework.c_validator import CustomUniqueValidator, CustomValidationError


def custom_exception_handler(exc, context):
    message = '服务器错误！'

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
                message = "未找到！"

        if response.status_code == 400:
            message = '输入错误！'

        elif response.status_code == 401:
            if hasattr(response, 'data'):
                data = response.data
                if isinstance(data, dict) and "detail" in data.keys():
                    print(data["detail"])
                    if data.get("detail") == "找不到指定凭据对应的有效用户":
                        message = "无效的用户名或密码！"

                    if data.get("detail") == "此令牌对任何类型的令牌无效":
                        message = "认证失败，请重新登录！"

                    if data.get("detail") == "身份认证信息未提供。":  # 身份认证信息未提供。
                        message = "登录已过期，请重新登录！"

                    if data.get("detail") == "令牌无效或已过期":  # 身份认证信息未提供。
                        message = "令牌无效或已过期！"

        elif response.status_code == 403:
            message = "没有相应的权限！"

        elif response.status_code == 405:
            message = '错误的请求方法！'

        elif response.status_code >= 500:
            message = "服务器错误！"
    return JsonResponse(msg=message, code=response.status_code)
