import base64

from captcha.views import CaptchaStore, captcha_image
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
TokenRefreshView
)

from apps.system.serializers import MyTokenObtainPairSerializer


class CaptchaAPIView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        hashkey = CaptchaStore.generate_key()
        try:
            # 获取图片id
            id_ = CaptchaStore.objects.filter(hashkey=hashkey).first().id
            imgage = captcha_image(request, hashkey)
            # 将图片转换为base64
            image_base = f"data:image/png;base64,{base64.b64encode(imgage.content).decode('utf-8')}"
            json_data = {"captcha_id": id_, "captcha_key": image_base}
            # 批量删除过期验证码
            # CaptchaStore.remove_expired()
        except Exception:
            json_data = None
        return Response(data=json_data)


class CaptchaRefreshAPIView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        new_key = CaptchaStore.pick()
        try:
            # 获取图片id
            id_ = CaptchaStore.objects.filter(hashkey=new_key).first().id
            imgage = captcha_image(request, new_key)
            # 将图片转换为base64
            image_base = f"data:image/png;base64,{base64.b64encode(imgage.content).decode('utf-8')}"
            json_data = {"captcha_id": id_, "captcha_key": image_base}
            # 批量删除过期验证码
            # CaptchaStore.remove_expired()
        except Exception:
            json_data = None
        return Response(data=json_data)


class LoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
class DecoratedTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)