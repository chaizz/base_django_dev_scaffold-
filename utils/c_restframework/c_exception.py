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

from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler, Response, status


def custom_exception_handler(exc, context):
    """
    统一返回错误格式
    """
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        status_code = response.status_code
        if isinstance(exc, ValidationError):
            message = exc.detail
        elif isinstance(exc, APIException):
            message = exc.default_detail
        else:
            message = response.data.get("detail", None)

    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = str(exc)

    data = {
        "status_code": status_code,
        "message": message,
        "data": {},
    }
    return Response(data, status=status_code)
