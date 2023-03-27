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

urlpatterns = [
    path('token-auth/', views.obtain_auth_token)

]
