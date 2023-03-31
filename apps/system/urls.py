"""
-------------------------------------------------
    File Name:   urls.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/27 13:51
-------------------------------------------------
    Change Activity:
          2023/3/27 13:51
-------------------------------------------------
"""
from django.urls import path, include
from rest_framework import routers

from apps.system.views import CaptchaAPIView, CaptchaRefreshAPIView, LoginTokenObtainPairView, \
    DecoratedTokenRefreshView, RegisterView, UsersViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UsersViewSet)

urlpatterns = [

    path('register', RegisterView.as_view(), name='auth_register'),

    path('login', LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', DecoratedTokenRefreshView.as_view(), name='token_refresh'),

    path('captcha', CaptchaAPIView.as_view(), name='captcha_api'),
    path('captcha/refresh', CaptchaRefreshAPIView.as_view(), name='captcha_refresh'),

    path('', include(router.urls)),
]
