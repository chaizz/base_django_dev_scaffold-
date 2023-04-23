"""
-------------------------------------------------
    File Name:   exception.py
    Description: 
        
    Author:      chaizz
    Date:        2023/4/21 11:45
-------------------------------------------------
    Change Activity:
          2023/4/21 11:45
-------------------------------------------------
"""
from enum import IntEnum


class ExceptionEnum(IntEnum):
    # 服务错误
    service_err = 500

    # celery 错误
    celery_err = 510
    celery_beat_err = 511
    celery_worker_err = 512
    celery_flower_err = 513


class CusException(Exception):
    code = ExceptionEnum.service_err.value
    message = "A server error occurred."


class SettingsException(CusException): ...


class OAuthException(CusException): ...