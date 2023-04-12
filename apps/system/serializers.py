"""
-------------------------------------------------
    File Name:   serializers.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/27 14:31
-------------------------------------------------
    Change Activity:
          2023/3/27 14:31
-------------------------------------------------
"""

import re

from captcha.models import CaptchaStore
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.system.models import Users
from utils.c_restframework.c_validator import CustomValidationError, CustomUniqueValidator

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    重写TokenObtainPairSerializer类的部分方法以实现自定义数据响应结构和payload内容
    """
    captcha_key = serializers.CharField(
        required=True,
        help_text="验证码图案"
    )
    captcha_id = serializers.CharField(
        required=True,
        write_only=True,
        help_text="验证码编码"
    )

    def validate_captcha_key(self, captcha_key):
        # 验证码验证
        try:
            captcha = captcha_key.lower()
        except:
            raise CustomValidationError("验证码错误")
        img_code = CaptchaStore.objects.filter(id=int(self.initial_data['captcha_id'])).first()
        if img_code and timezone.now() > img_code.expiration:
            raise CustomValidationError("验证码已过期")
        if not img_code or img_code.response != captcha:
            raise CustomValidationError("验证码错误")

    @classmethod
    def get_token(cls, user):
        """
        此方法往token的有效负载 payload 里面添加数据
        例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
        这部分放在token里面是可以被解析的，所以不要放比较私密的信息

        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        token['name'] = user.username
        return token

    def validate(self, attrs):
        """
        此方法为响应数据结构处理
        原有的响应数据结构无法满足需求，在这里重写结构如下：
        {
            "refresh": "xxxx.xxxxx.xxxxx",
            "access": "xxxx.xxxx.xxxx",
            "expire": Token有效期截止时间,
            "username": "用户名",
            "email": "邮箱"
        }

        :param attrs: 請求參數
        :return: 响应数据
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['expire'] = refresh.access_token.payload['exp']  # 有效期
        data['username'] = self.user.username

        return data


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class RegisterSerializer(serializers.ModelSerializer):
    """
    每个字段设置为 write_only , 反序列化不返回字段。
    """
    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="该邮箱已注册")]
    )
    username = serializers.CharField(
        write_only=True,
        required=True,
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="该用户名已存在")]
    )

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ("username", 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise CustomValidationError({"password": "两次密码不一致"})
        return attrs

    def validate_password(self, value):
        "正则匹配密码"
        if re.search(r"^[a-zA-Z]{1}([a-zA-Z0-9]|[._]){5,29}$", value):
            return value
        else:
            raise CustomValidationError("密码不符合规则：必须字母开头，6到30个字符，必须包含数字下划线点")

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data["email"],
            password=validated_data['password']
        )
        user.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class OtherUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("nickname", "introduction")


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    """
    用户修改-序列化器
    """
    phone_number = serializers.CharField(
        max_length=11,
        validators=[
            CustomUniqueValidator(queryset=Users.objects.all(), message="手机号必须唯一")
        ],
        allow_blank=True
    )

    email = serializers.EmailField(
        required=True,
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="该邮箱已注册")]
    )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Users
        fields = ['nickname',
                  'introduction',
                  'gender',
                  'phone_number',
                  'gender',
                  'birthday',
                  'email'
                  ]
