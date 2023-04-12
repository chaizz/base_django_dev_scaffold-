import base64

from captcha.views import CaptchaStore, captcha_image
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework.exceptions import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from apps.system.models import Users
from apps.system.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserInfoUpdateSerializer
from apps.system.serializers import UserInfoSerializer, OtherUserInfoSerializer
from utils.c_restframework.c_generics import CustomListCreateAPIView
from utils.c_restframework.c_modelviewset import CustomModelViewSet
from utils.c_restframework.c_permission import IsOwnerOrReadOnly, IsAdminPermission
from utils.c_restframework.c_response import JsonResponse, ErrorResponse


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


class RegisterView(CustomListCreateAPIView):
    queryset = Users.objects.all()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UsersViewSet(CustomModelViewSet):
    serializer_class = UserInfoSerializer
    queryset = Users.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance or request.user.is_superuser:
            serializer = UserInfoSerializer(instance)
        else:
            serializer = OtherUserInfoSerializer(instance)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdminPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=["PUT"], detail=True, permission_classes=[IsAuthenticated], url_name="change_password")
    def change_password(self, request, *args, **kwargs):
        """
        管理员修改用户密码
        """
        data = request.data
        new_pwd = data.get("newPassword")
        new_pwd2 = data.get("newPassword2")
        if new_pwd != new_pwd2:
            return ErrorResponse(msg="两次密码不匹配")
        request.user.password = make_password(new_pwd)
        request.user.save()
        return JsonResponse(data=None, msg="修改成功")

    @action(methods=["PUT"], detail=False, permission_classes=[IsAuthenticated], url_name="update_info")
    def update_user_info(self, request):
        """修改当前用户信息"""
        serializer = UserInfoUpdateSerializer(request.user, data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=None, msg="修改成功")
