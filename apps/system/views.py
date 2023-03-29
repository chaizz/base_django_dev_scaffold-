import base64
from rest_framework.decorators import action

from captcha.views import CaptchaStore, captcha_image
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import status
from utils.c_restframework.c_response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from apps.system.models import Users
from apps.system.serializers import MyTokenObtainPairSerializer, RegisterSerializer, PasswordSerializer
from apps.system.serializers import UserInfoSerializer
from utils.c_restframework.c_permission import IsAdminPermission


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
        return JsonResponse(data=json_data)


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
        return JsonResponse(data=json_data)


class LoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return JsonResponse(response.data)

class DecoratedTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return JsonResponse(response.data)


class RegisterView(CreateAPIView):
    queryset = Users.objects.all()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = UserInfoSerializer
    queryset = Users.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdminPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(methods=['post'], detail=True, permission_classes=[],
            url_path='change_password', url_name='change_password')
    def set_password(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            raise
        user.save()
        return Response(serializer.data)
