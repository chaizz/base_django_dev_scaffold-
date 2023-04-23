"""
-------------------------------------------------
    File Name:   urls.py
    Description: 
        
    Author:      chaizz
    Date:        2023/4/23 13:50
-------------------------------------------------
    Change Activity:
          2023/4/23 13:50
-------------------------------------------------
"""
from django.urls import path, include
from rest_framework import routers


from .views import GitHubOAuthView

urlpatterns = [
    path('github', GitHubOAuthView.as_view(), name='github_auth'),

]