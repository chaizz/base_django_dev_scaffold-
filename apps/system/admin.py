from django.contrib import admin

from apps.system.models import Users


@admin.register(Users)
class UserProfileAdmin(admin.ModelAdmin):
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
