import os
from json import load
from pathlib import Path
from typing import Union, Tuple, List, Literal
from pydantic import BaseModel

PATH = Path(os.getcwd())

CONFIG_PATH = PATH / "config" / "config.json"


class DateConfig(BaseModel, extra="ignore"):
    year: int = 2024
    month: int = 6
    day: int = 7
    hour: int = 0
    minute: int = 0


class FontStyleConfig(BaseModel, extra="ignore"):
    size: int
    pos: Tuple[float, float]
    fill_color: Tuple[int, int, int]


class DateStyleConfig(BaseModel, extra="ignore"):
    day: FontStyleConfig
    hour_and_minute: FontStyleConfig


class Config(BaseModel, extra="ignore"):
    """基础配置类，提供基础的配置"""

    update_time: Union[float, int] = 30
    auto_update: bool = True
    plugin_path: str = "./plugin"
    gaokao_image_path: str = "./image/高考.png"
    shoukao_image_path: str = "./image/首考.png"
    background_image_path: str = "./image/background.png"
    cache_path: str = "./cache/image.png"
    font_path: str = "./font/AaWuHunTi-2.ttf"
    log_path: str = "./logs/latest.log"
    one_word_api: str = "https://tenapi.cn/v2/yiyan?format=json"
    gaokao_date: DateConfig = DateConfig(day=7, month=6)
    shoukao_date: DateConfig = DateConfig(day=6, month=1)
    latest_date: DateConfig = DateConfig()
    now_state: Literal["高考", "首考"] = "高考"
    one_word: str = ""
    words: List[str] = ["本地一言库可以自己改哦\n————请遵循格式！"]
    word_style: FontStyleConfig = FontStyleConfig(
        **{"size": 60, "pos": [2000, 1850], "fill_color": [234, 72, 114]}
    )

    style: DateStyleConfig = DateStyleConfig(
        **{
            "day": FontStyleConfig(
                **{"size": 400, "pos": [2000, 1100], "fill_color": [255, 60, 36]}
            ),
            "hour_and_minute": FontStyleConfig(
                **{"size": 200, "pos": [2000, 1400], "fill_color": [153, 153, 153]}
            ),
        }
    )

    def __getitem__(self, key):
        """兼容字典调用方法"""
        print("正在调用Config字典调用方法！")
        return self.model_dump()[key]

    class Config:
        env_file = ".json"


def get_config() -> Config:
    with open(CONFIG_PATH, "r+", encoding="utf-8") as file:
        return Config(**load(file))


def update_config(new_config: Config) -> None:
    with open(CONFIG_PATH, "w+", encoding="utf-8") as file:
        file.write(str(new_config.model_dump_json(indent=4)))


if not os.path.exists(CONFIG_PATH.parent):
    os.mkdir(CONFIG_PATH.parent)

if not os.path.exists(CONFIG_PATH):
    f = open(CONFIG_PATH, "x", encoding="utf-8")
    f.close()
    with open(CONFIG_PATH, "w+", encoding="utf-8") as f:
        f.write(str(Config().model_dump_json(indent=4)))
