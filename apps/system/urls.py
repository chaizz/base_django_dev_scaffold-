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
from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]
