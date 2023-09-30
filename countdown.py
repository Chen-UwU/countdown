import os
import time
import ctypes

from json import load
from typing import Tuple
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image

DEFAULT_CONFIG_PATH = os.getcwd() + "/config/config.json"
FONT_PATH = os.getcwd() + "/font/AaLingJunTi-2.ttf"
CACHE_PATH = os.getcwd() + "/cache/image.png"
WALLPAPER_PATH = os.getcwd() + "/image/image.jpg"
CONFIG_PATH = os.getcwd() + "/config/config.json"
LOG_PATH = os.getcwd() + "/log/latest.log"


def get_weather():
    """获取每日天气"""


def get_daily_words():
    """获取每日格言"""


def get_config(config_path=DEFAULT_CONFIG_PATH):
    """获取配置信息"""
    f = open(CONFIG_PATH, "r", encoding="utf-8")
    config = load(f)
    f.close()
    return config


def countdown() -> Tuple[int, int, int]:
    """
    获得倒计时
    返回元组含义：日，小时，分钟。
    """
    now = datetime.now()
    feature = datetime(2024, 1, 6, 0, 0)
    diff = feature - now
    second = int(diff.total_seconds())
    day = second // 86400
    hour = second % 86400 // 3600
    minute = second % 86400 // 60 % 60
    print(day, hour, minute)
    return day, hour, minute


def generate_wallpaper() -> str:
    """生成壁纸"""
    time_diff = countdown()
    image = Image.open(WALLPAPER_PATH)
    font = ImageFont.truetype(FONT_PATH, 300)
    draw = ImageDraw.Draw(image)
    draw.text((1180, 520), str(time_diff[0]), font=font, fill=(237, 28, 36))
    font = ImageFont.truetype(FONT_PATH, 200)
    draw.text((960, 1050), str(time_diff[1]), font=font, fill=(237, 28, 36))
    draw.text((1300, 1050), str(time_diff[2]), font=font, fill=(237, 28, 36))
    image.save(CACHE_PATH)
    return CACHE_PATH


def change_wallpaper(path: str):
    """更换壁纸"""
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def main() -> int:
    f = open(LOG_PATH, "w+", encoding="utf-8")
    try:
        while True:
            image_path = generate_wallpaper()
            change_wallpaper(image_path)
            f.write("执行成功:" + str(countdown()) + "\n")
            time.sleep(get_config()["update_time"])
            f.flush()
    except Exception as e:
        f.write("Bad quit:" + str(e) + "\n")
        f.flush()
        return 1
    finally:
        f.close()


if __name__ == "__main__":
    main()
