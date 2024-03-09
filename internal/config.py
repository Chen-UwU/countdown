import os
from json import load
from pathlib import Path
from typing import Union, Tuple, List
from pydantic import BaseModel

PATH = Path(os.getcwd())

CONFIG_PATH = PATH / "config" / "config.json"


class DateConfig(BaseModel, extra="ignore"):
    year: int = 2024
    month: int = 6
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


class Config(BaseModel, extra="ignore"):
    """基础配置类，提供基础的配置"""

    update_time: Union[float, int] = 30
    auto_update: bool = True
    plugin_path: str = "./plugin"
    image_path: str = "./image/高考.png"
    cache_path: str = "./cache/image.png"
    font_path: str = "./font/AaLingJunTi-2.ttf"
    log_path: str = "./logs/latest.log"
    date: DateConfig = DateConfig()
    latest_date: DateConfig = DateConfig()
    one_word: str = ""
    words: List[str] = [""]
    word_style: FontStyleConfig = FontStyleConfig(
        **{"size": 30, "pos": [425, 770], "fill_color": [234, 72, 229]}
    )
    style: DateStyleConfig = DateStyleConfig(
        **{
            "day": FontStyleConfig(
                **{"size": 150, "pos": [280, 560], "fill_color": [237, 28, 36]}
            ),
            "hour": FontStyleConfig(
                **{"size": 110, "pos": [730, 560], "fill_color": [237, 28, 36]}
            ),
            "minute": FontStyleConfig(
                **{
                    "size": 80,
                    "pos": [1200, 580],
                    "fill_color": [237, 28, 36],
                },
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
    with open(CONFIG_PATH, "r+", encoding="utf-8") as f:
        return Config(**load(f))


def update_config(new_config: Config) -> None:
    with open(CONFIG_PATH, "w+", encoding="utf-8") as f:
        f.write(str(new_config.model_dump_json(indent=4)))


if not os.path.exists(CONFIG_PATH.parent):
    os.mkdir(CONFIG_PATH.parent)

if not os.path.exists(CONFIG_PATH):
    f = open(CONFIG_PATH, "x", encoding="utf-8")
    f.close()
    with open(CONFIG_PATH, "w+", encoding="utf-8") as f:
        f.write(str(Config().model_dump_json(indent=4)))
