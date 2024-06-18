import os
import ctypes
from typing_extensions import override

from internal.adapter import Adapter
from internal.logger import logger


def change_wallpaper(path: str) -> None:
    """更换壁纸"""
    if path[0] == ".":
        path = os.getcwd() + path[1:]
    logger.info(f"更换壁纸中，壁纸位置:{path}")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    logger.info("更换壁纸完成。")


class WinWallpaperAdapter(Adapter):

    @override
    def get_name(self):
        return "Win_Wallpaper"

    @override
    async def async_update_wallpaper(self, path: str) -> None:
        """更换壁纸"""
        change_wallpaper(path)

    def update_wallpaper(self, path: str) -> None:
        """更换壁纸"""
        change_wallpaper(path)
