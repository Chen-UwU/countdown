import os
import time
import ctypes

from datetime import datetime
from PIL import ImageFont, ImageDraw, Image

from config import CONFIG, DateConfig, FontStyleConfig, get_updated_config 

def countdown(date: DateConfig) -> DateConfig:
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
    print(day, hour, minute)
    return DateConfig(
        **{"year": 0, "month": 0, "day": day, "hour": hour, "minute": minute}
    )


def generate_wallpaper(time_diff: DateConfig) -> str:
    """生成壁纸"""
    image = Image.open(CONFIG.image_path)
    draw = ImageDraw.Draw(image)
    for key, value in time_diff.model_dump().items():
        try:
            font_style = FontStyleConfig(**CONFIG.style.date_style.model_dump()[key])
        except KeyError:
            continue
        print(font_style)
        font = ImageFont.truetype(CONFIG.font_path, font_style.size)
        draw.text(
            font_style.pos,
            str(value),
            font=font,
            fill=font_style.fill_color,
            align="center",
        )
    image.save(CONFIG.cache_path)
    return CONFIG.cache_path


def change_wallpaper(path: str) -> None:
    """更换壁纸"""
    if path[0] == ".":  # 如果是相对路径
        path = os.getcwd() + path[1:]
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def main() -> int:
    global CONFIG
    f = open(CONFIG.log_path, "w+", encoding="utf-8")
    try:
        while True:
            CONFIG = get_updated_config()
            time_diff = countdown(CONFIG.style.date)
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
