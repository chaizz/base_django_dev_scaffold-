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

from rest_framework import permissions

logger = logging.getLogger(__name__)


class IsAdminPermission(permissions.BasePermission):
    """
    判断是否是超级管理员权限
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限，只允许对象的所有者编辑它。
    假设模型实例有一个“user”属性。
    """
    def has_object_permission(self, request, view, obj):
        # 所以我们总是允许GET、HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True

        # 否则我们就判断, 当前数据的用户名是否跟当前用户一致
        # 实例必须有一个名为“user”的属性。
        # model实例obj
        print(object.user == request.user)
        return obj.user == request.user
