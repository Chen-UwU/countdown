import os
import time
import ctypes

from json import load
from typing import Tuple
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image

FONT_PATH = os.getcwd() + "/font/AaLingJunTi-2.ttf"
Cache_PATH = os.getcwd() + "/cache/image.png"
WALLPAPER_PATH = os.getcwd() + "/image/image.jpg"

def get_config():
    ...

def cutdown()->Tuple[int,int,int]: # 日，小时，分钟。
    now = datetime.now()
    feature = datetime(2024,1,6,0,0)
    diff = feature-now
    second = int(diff.total_seconds())
    day = second // 86400
    hour = second % 86400 // 3600
    minute = second % 86400 // 60 % 60
    print(day,hour,minute)
    return day,hour,minute

def generate_wallpaper()->str:
    time_diff = cutdown()
    image = Image.open(WALLPAPER_PATH)
    font = ImageFont.truetype(FONT_PATH, 300)
    draw = ImageDraw.Draw(image)
    draw.text((1180, 520), str(time_diff[0]), font=font, fill=(237,28,36))
    font = ImageFont.truetype(FONT_PATH, 200)
    draw.text((960, 1050), str(time_diff[1]), font=font, fill=(237,28,36))
    draw.text((1300, 1050), str(time_diff[2]), font=font, fill=(237,28,36))
    image.save(Cache_PATH)
    return Cache_PATH
    
def change_wallpaper(path:str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    
if __name__ == '__main__':
    
    while True:
        image_path = generate_wallpaper()
        change_wallpaper(image_path)
        time.sleep(59)