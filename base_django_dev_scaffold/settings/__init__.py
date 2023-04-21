"""
-------------------------------------------------
    File Name:   __init__.py.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/24 14:54
-------------------------------------------------
    Change Activity:
          2023/3/24 14:54
-------------------------------------------------
"""
import os
from pathlib import Path

from utils.common.exception import SettingsException


def set_environ(env="dev"):
    """
        添加settings下的配置文件。
    """
    parent_dir = Path(__file__).resolve().parent
    settings_path = Path(parent_dir, f"{env}.py")
    if not settings_path.is_file():
        raise SettingsException("无法获取配置文件！")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"base_django_dev_scaffold.settings.{env}")
