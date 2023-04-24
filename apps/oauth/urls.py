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
from django.urls import path

from .views import DingTalkOAuthView, GitHubOAuthView

urlpatterns = [
    path('github', GitHubOAuthView.as_view(), name='github_oauth'),
    path('dingtalk', DingTalkOAuthView.as_view(), name='dingtalk_oauth'),
]
