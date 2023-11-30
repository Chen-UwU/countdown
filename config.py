import os
from json import load
from typing import Union, Tuple
from pydantic import BaseModel

PATH = os.getcwd()

CONFIG_PATH = PATH + "\\config\\config.json"


class DateConfig(BaseModel, extra="ignore"):
    year: int = 2024
    month: int = 1
    day: int = 6
    hour: int = 0
    minute: int = 0


class FontStyleConfig(BaseModel, extra="ignore"):
    size: int
    pos: Tuple[float, float]
    fill_color: Tuple[int, int, int]


class DateStyleConfig(BaseModel, extra="ignore"):
    day: FontStyleConfig
    hour: FontStyleConfig
    minute: FontStyleConfig


class StyleConfig(BaseModel, extra="ignore"):
    date_style: DateStyleConfig
    date: DateConfig


class Config(BaseModel, extra="ignore"):
    """基础配置类，提供基础的配置"""

    update_time: Union[float, int] = 60
    auto_update: bool = True
    plugin_path: str = "./plugin"
    image_path: str = "./image/image.jpg"
    cache_path: str = "./cache/image.png"
    font_path: str = "./font/AaLingJunTi-2.ttf"
    log_path: str = "./log/latest.log"
    style: StyleConfig = StyleConfig(
        **{
            "date": {"year": 2024, "month": 1, "day": 6, "hour": 0, "minute": 0},
            "date_style": {
                "day": {"size": 300, "pos": [1180, 520], "fill_color": [237, 28, 36]},
                "hour": {"size": 200, "pos": [960, 1050], "fill_color": [237, 28, 36]},
                "minute": {
                    "size": 200,
                    "pos": [1300, 1050],
                    "fill_color": [237, 28, 36],
                },
            },
        }
    )

    def __getitem__(self, key):
        return self.model_dump()[key]

    class Config:
        env_file = ".json"


def get_updated_config() -> Config:
    with open(CONFIG_PATH, "r+") as f:
        return Config(**load(f))


def update_config() -> None:
    with open(CONFIG_PATH, "r+") as f:
        global CONFIG
        CONFIG = Config(**load(f))

if not os.path.exists(CONFIG_PATH):
    os.mkdir("config")
    with open(CONFIG_PATH, "w+") as f:
        f.write(str(Config().model_dump_json(indent=True))) 

with open(CONFIG_PATH, "r+") as f:
    CONFIG = Config(**load(f))
