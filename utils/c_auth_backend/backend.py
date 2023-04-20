"""
-------------------------------------------------
    File Name:   backend.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/27 17:27
-------------------------------------------------
    Change Activity:
          2023/3/27 17:27
-------------------------------------------------
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class MyModelBackendBackend(ModelBackend):
    """
    添加邮箱和用户名登录校验
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) & Q(is_active=True))
            if user.check_password(password):
                return user
        except Exception:
            return None
