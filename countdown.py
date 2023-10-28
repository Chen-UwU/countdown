import os
import time
import ctypes

from json import load
from typing import Dict
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image

DEFAULT_CONFIG_PATH = os.getcwd() + "/config/config.json"
FONT_PATH = os.getcwd() + "/font/AaLingJunTi-2.ttf"
CACHE_PATH = os.getcwd() + "/cache/image.png"
WALLPAPER_PATH = os.getcwd() + "/image/image.jpg"
LOG_PATH = os.getcwd() + "/log/latest.log"

with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = load(f)


def countdown(date:dict) -> Dict[str, int]:
    """
    获得倒计时
    返回元组含义：日，小时，分钟。
    """
    now = datetime.now()
    future = datetime(date["year"], date["month"], date["day"],
                      date["hour"], date["minute"])
    diff = future - now
    second = int(diff.total_seconds())
    day = second // 86400
    hour = second % 86400 // 3600
    minute = second % 86400 // 60 % 60
    print(day, hour, minute)
    return {"day":day,"hour":hour,"minute":minute}


def generate_wallpaper(time_diff:dict) -> str:
    """生成壁纸"""
    image = Image.open(WALLPAPER_PATH)
    draw = ImageDraw.Draw(image)
    for key, value in time_diff.items():
        font_style = CONFIG["font_style"][key]
        print(font_style)
        font = ImageFont.truetype(FONT_PATH, font_style["size"])
        draw.text(tuple(font_style["pos"]), str(value), font=font,
                  fill=tuple(font_style["fill_color"]))
    image.save(CACHE_PATH)
    return CACHE_PATH


def change_wallpaper(path: str) -> None:
    """更换壁纸"""
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def main() -> int:
    f = open(LOG_PATH, "w+", encoding="utf-8")
    try:
        while True:
            time_diff = countdown(CONFIG["date"])
            image_path = generate_wallpaper(time_diff)
            change_wallpaper(image_path)
            f.write("执行成功:" + str(time_diff) + "\n")
            time.sleep(CONFIG["update_time"])
            f.flush()
    except Exception as e:
        f.write("Bad quit:" + str(e) + "\n")
        f.flush()
        return 1
    finally:
        f.close()


if __name__ == "__main__":
    main()
