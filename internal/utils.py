import os
import ctypes
import random
import requests

from json import loads
from typing import Dict
from datetime import datetime

from .config import get_config, update_config, DateConfig
from .logger import logger


def countdown(date: DateConfig) -> Dict[str, int]:
    """
    获得倒计时
    返回元组含义：日，小时，分钟。
    """
    now = datetime.now()
    future = datetime(date.year, date.month, date.day, date.hour, date.minute)
    diff = future - now
    second = int(diff.total_seconds())
    day = second // 86400
    hour = second % 86400 // 3600
    minute = second % 86400 // 60 % 60
    logger.debug("倒计时天数：" + str([day, hour, minute]))
    return {"day": day, "hour": hour, "minute": minute}


def get_word():
    """
    获取每日一言
    API接口调用超过120/min时会被自动拉黑5min
    """
    now = datetime.now()
    config = get_config()
    if config.latest_date.day != now.day:
        logger.info(f"配置日期：{config.latest_date.day}，今日日期：{now.day}")
        config.latest_date = DateConfig(year=now.year, month=now.month, day=now.day)
        try:
            res = requests.get("https://tenapi.cn/v2/yiyan?format=json", timeout=100)
            result = loads(res.content.decode("utf-8"))
            one_word = result["data"]["hitokoto"] + "\n——" + result["data"]["author"]
        except:
            one_word = random.choice(config.words)
            config.words.remove(one_word)
            config.one_word = one_word
        update_config(config)
        logger.info("新每日一言已生成：{}".format(one_word))
        return one_word
    else:
        return config.one_word


def change_wallpaper(path: str) -> None:
    """更换壁纸"""
    if path[0] == ".":
        path = os.getcwd() + path[1:]
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
