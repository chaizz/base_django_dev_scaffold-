from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db import models


class MyUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        创建普通用户
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError('Users must have an email address')

        return self._create_user(username, email, password, **extra_fields)


class Users(AbstractUser):
    # 删除字段
    first_name = None
    last_name = None

    gender_choices = (
        ('0', '未知'),
        ('1', '男'),
        ('2', '女')
    )
    nickname = models.CharField(max_length=30, db_column='nickname', null=True, blank=False, verbose_name='昵称',
                                help_text='昵称，不超过30个字符')
    introduction = models.CharField(max_length=100, db_column='introduction', null=True, blank=False,
                                    verbose_name='个人简介',
                                    help_text='个人简介，不超过100个字符')
    gender = models.CharField(max_length=2, choices=gender_choices, db_column='gender', default=0, verbose_name='性别',
                              help_text='性别，默认为未知。')
    phone_number = models.CharField(max_length=50, db_column='phone_number', null=True, blank=True,
                                    verbose_name='联系方式', help_text='手机号')
    birthday = models.DateField(db_column='birthday', null=True, blank=True, verbose_name='出生日期',
                                help_text='出生日期')

    email = models.EmailField(max_length=100, db_column='email', unique=True, verbose_name='邮箱',
                              help_text='邮箱，不超过100个字符')

    date_joined = models.DateTimeField(db_column='date_joined', auto_now_add=True, verbose_name='用户加入时间',
                                       help_text='用户注册时间')

    avatar_url = models.CharField(max_length=255, null=True, blank=True, db_column='avatar_url',
                                  verbose_name='头像地址',
                                  help_text='头像地址，不超过255个字符')

    def __str__(self):
        return self.nickname or self.username

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = MyUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = '用户基础信息'
        verbose_name_plural = verbose_name
        ordering = ['id']
