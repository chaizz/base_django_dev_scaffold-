from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

Users = get_user_model()


class SocialAccount(models.Model):
    """
    社交账户相关信息
    """

    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户', help_text="关联用户")
    uid = models.CharField(db_column="uid", max_length=120, verbose_name='第三方账号ID', unique=True, blank=True,
                                         help_text="第三方账号ID：微信、QQ、Github等")

    open_id = models.CharField(db_column="open_id", max_length=120,  verbose_name='第三方账号open ID', unique=True, blank=True,
                                         help_text="第三方账号open ID：微信、QQ、Github等")

    email = models.EmailField(max_length=100, db_column='email', unique=True, verbose_name='邮箱',
                              help_text='邮箱，不超过100个字符')

    nickname = models.CharField(max_length=30, db_column='nickname', null=True, blank=False, verbose_name='昵称',
                                help_text='昵称，不超过30个字符')

    account_type = models.CharField(db_column='account_type', max_length=255, blank=True,
                                    verbose_name='第三方账号类型', help_text='第三方账号类型')
    phone_number = models.CharField(max_length=50, db_column='phone_number', null=True, blank=True,
                                    verbose_name='联系方式', help_text='手机号')
    avatar_url = models.CharField(max_length=255, null=True, blank=True, db_column='avatar_url',
                                  verbose_name='头像地址',
                                  help_text='头像地址，不超过255个字符')
    create_time = models.DateTimeField(db_column='create_time', auto_now_add=True, verbose_name='用户加入时间',
                                       help_text='第三方账号用户加入时间')

    def __str__(self):
        return self.uid or self.uid

    class Meta:
        db_table = 'social_account'
        verbose_name = '第三方账号'
        verbose_name_plural = verbose_name
        ordering = ['id']
