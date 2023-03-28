from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.system.models import Users


@admin.register(Users)
class UserProfileAdmin(UserAdmin):
    list_display = ("username", "nickname", "gender", "email", "phone_number")
    list_display_links = ("username", "nickname")
    list_filter = ("phone_number",)
    search_fields = ["nickname", "phone_number", "email"]

    filter_horizontal = ("groups", "user_permissions")  #

    fieldsets = (
        ("账号密码", {
            "fields": (("username", "password"),)
        }),
        ("基本信息", {
            "fields": ("nickname", "gender", "birthday", "email", "phone_number")
        }
         ),

        ("其他", {
            "fields": ("is_superuser", "is_staff", "is_active")
        }
         ),
        ("用户组/权限", {
            "fields": ("groups", "user_permissions")
        }
         ),

    )


admin.site.site_header = "Django 开发脚手架"  # 设置header
admin.site.site_title = 'Django 开发脚手架'  # 设置title
admin.site.index_title = 'Django 开发脚手架'
