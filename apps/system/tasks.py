"""
-------------------------------------------------
    File Name:   tasks.py
    Description: 
        
    Author:      chaizz
    Date:        2023/4/20 14:03
-------------------------------------------------
    Change Activity:
          2023/4/20 14:03
-------------------------------------------------
"""
from captcha.views import CaptchaStore

from celery import shared_task


@shared_task
def delete_expired_captcha():
    # 批量删除过期验证码
    CaptchaStore.remove_expired()


@shared_task
def add(x, y):
    # 批量删除过期验证码
    print(x + y)
    return x+y