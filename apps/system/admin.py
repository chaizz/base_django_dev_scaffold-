from django.contrib import admin

from apps.system.models import Users


@admin.register(Users)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "nickname", "gender", "email", "phone_number")
    list_display_links = ("username",)
    list_filter = ("phone_number",)
    search_fields = ["nickname"]

    filter_horizontal = ("roles",)  # 多对多字段 使用双向选择器  水平方向
    fieldsets = (
        ("账号密码", {
            "fields": (("username", "password"),)
        }),
        ("基本信息", {
            "fields": ("nickname", "gender", "birthday", "email", "phone_number", "ethnicity", "avatar_url")
        }
         ),
        ("地址", {
            "fields": ("province", "city", "area", "town", "address")
        }
         ),

        ("部门/权限", {
            "fields": ("roles", "dept")
        }
         ),

        ("其他", {
            "fields": ("is_superuser", "is_staff", "is_active")
        }
         ),

    )
