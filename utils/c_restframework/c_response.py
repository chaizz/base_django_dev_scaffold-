"""
-------------------------------------------------
    File Name:   c_response.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/29 10:22
-------------------------------------------------
    Change Activity:
          2023/3/29 10:22
-------------------------------------------------
"""
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=200, msg="success", status=None, template_name=None, headers=None, exception=False,
                 content_type=None, **kwargs):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        # 兼容如果msg是字典， 将字典改为 字符串
        if isinstance(msg, dict):
            msg = "".join(''.join(v) for k, v in msg.items() if isinstance(v, list))
        # 修改Response的 data格式
        self.data = {"code": code, "message": msg, "data": data} | kwargs
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回400, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(self, data=None, msg='error', code=400, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)