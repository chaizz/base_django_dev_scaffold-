"""
-------------------------------------------------
    File Name:   c_permission.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/28 16:12
-------------------------------------------------
    Change Activity:
          2023/3/28 16:12
-------------------------------------------------
"""
import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsAdminPermission(BasePermission):
    """
    判断是否是超级管理员权限
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_superuser)

