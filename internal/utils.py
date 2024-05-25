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
    logger.debug(f"倒计时天数:{str([day, hour, minute])}")
    return {"day": day, "hour": hour, "minute": minute}


def get_word():
    """
    获取每日一言
    API接口调用超过120/min时会被自动拉黑5min
    """
    now = datetime.now()
    seed = (now - datetime(2006, 6, 2)).days  # 小彩蛋XD
    random.seed(seed)  # 确立随机数种子保证每天的一言所有电脑都是一样的
    config = get_config()

    if config.latest_date.day != now.day:
        logger.info(f"配置日期：{config.latest_date}，今日日期：{now}")
        config.latest_date = DateConfig(year=now.year, month=now.month, day=now.day)
        try:
            res = requests.get(config.one_word_api, timeout=100)
            result = loads(res.content.decode("utf-8"))
            one_word = result["data"]["hitokoto"] + "\n——" + result["data"]["author"]
            logger.info("从互联网获取一言成功")
            config.words.append(one_word)
        except requests.exceptions.ConnectionError:
            logger.warning("访问互联网失败，正在从本地获取一言。")
            one_word = random.choice(config.words)
        config.one_word = one_word
        update_config(config)
        logger.info(f"新每日一言已生成：{repr(one_word)}")
        return one_word
    else:
        return config.one_word


def change_wallpaper(path: str) -> None:
    """更换壁纸"""
    if path[0] == ".":
        path = os.getcwd() + path[1:]
    logger.info(f"更换壁纸中，壁纸位置:{path}")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    logger.info("更换壁纸完成。")


def check_time() -> None:
    """时间检查器，检查时间是高考还是首考。"""
    now = datetime.now()
    config = get_config()
    gaokao_time = datetime(now.year, config.gaokao_date.month, config.gaokao_date.day)
    shoukao_time = (
        datetime(now.year + 1, config.shoukao_date.month, config.shoukao_date.day)
        if now <= datetime(now.year, 12, 31)
        else datetime(now.year, config.shoukao_date.month, config.shoukao_date.day)
    )

    if now < shoukao_time:
        config.now_state = "首考"
        config.gaokao_date.year = shoukao_time.year
    elif now < gaokao_time:
        config.now_state = "高考"
        config.gaokao_date.year = gaokao_time.year

    if config == get_config():
        update_config(config)

def open_info() -> None:
    """给出info并打开文件

    此函数为不知情的用户设计。因为还没有开发出UI，所以使用os.system调用系统软件来打开txt文件夹作为info

    """
    config = get_config()
    seed = (datetime.now() - datetime(2006, 6, 2)).days
    random.seed(seed)
    
    if  not os.path.exists(config.info_file):
        return
    if random.randint(0,30) == 1: # 不是每一天都得开（虽然随机开有点智障）
        os.system("start " + config.info_file)