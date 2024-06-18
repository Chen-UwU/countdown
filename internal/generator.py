import os

from pathlib import Path
from typing import Dict, Tuple
from PIL import ImageFont, ImageDraw, Image
from cn2an import an2cn

from .config import get_config, FontStyleConfig
from .logger import logger
from .utils import get_word

import os


def centered(
    pos: Tuple[float, float], box: Tuple[int, int, int, int]
) -> Tuple[float, float]:
    """使一个图片的位置转化为居中的位置

    Args:
        pos (Tuple[float, float]): 想要居中的位置
        box (Tuple[int, int, int, int]): 图片的box大小

    Returns:
        Tuple[float, float]: 居中的位置
    """
    h, w = abs(box[1] - box[3]), abs(box[0] - box[2])
    pos = (pos[0] - w / 2, pos[1] - h / 2)
    return pos


def generate_wallpaper(time_diff: Dict[str, int]) -> str:
    """生成壁纸"""
    config = get_config()

    if config.now_state == "高考":
        image = Image.open(config.gaokao_image_path)
    else:
        image = Image.open(config.shoukao_image_path)
    draw = ImageDraw.Draw(image)
    values = [
        an2cn(time_diff["day"]),
        f"{an2cn(time_diff['hour'])}小时{an2cn(time_diff['minute'])}分钟",
    ]

    for key, value in zip(config.style.model_dump(), values):
        font_style: FontStyleConfig = FontStyleConfig(**config.style.model_dump()[key])
        logger.debug(f"对{key}的字体风格:{str(font_style)}")
        font = ImageFont.truetype(config.font_path, font_style.size)
        draw.text(
            centered(font_style.pos, font.getbbox(value)),
            value,
            font=font,
            fill=font_style.fill_color,
        )

    word = get_word()
    if word is not None:
        font = ImageFont.truetype(config.font_path, config.word_style.size)
        draw.text(
            centered(config.word_style.pos, font.getbbox(word.splitlines()[0])),
            word,
            font=font,
            fill=config.word_style.fill_color,
            align="center",
        )

    background = Image.open(config.background_image_path)
    background = background.resize(image.size)
    image = image.convert("RGBA")
    background = background.convert("RGBA")
    mask = image.split()[3]
    background.paste(image, (0, 0), mask)

    cache_path = Path(config.cache_path)
    if not os.path.exists(cache_path.parent):
        os.makedirs(cache_path.parent)

    background.save(config.cache_path)
    return config.cache_path
