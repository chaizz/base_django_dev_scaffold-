from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

Users = get_user_model()


class SocialAccount(models.Model):
    """
    社交账户相关信息
    """
    user = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name='用户', help_text="关联用户")
    avatar_url = models.CharField(max_length=255, null=True, blank=True, db_column='avatar_url',
                                  verbose_name='头像地址',
                                  help_text='github头像地址')
    github_id = models.PositiveBigIntegerField(db_column="github_id", verbose_name='GitHub id', unique=True, blank=True,
                                               help_text="Github ID")
