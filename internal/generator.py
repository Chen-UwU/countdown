from PIL import ImageFont, ImageDraw, Image
from typing import Dict
from cn2an import an2cn

from .config import get_config, FontStyleConfig
from .logger import logger
from .utils import get_word


def generate_wallpaper(time_diff: Dict[str, int]) -> str:
    """生成壁纸"""
    config = get_config()
    image = Image.open(config.image_path)
    draw = ImageDraw.Draw(image)
    for key, value in time_diff.items():
        font_style: FontStyleConfig = FontStyleConfig(**config.style.model_dump()[key])
        logger.debug(str(font_style))
        font = ImageFont.truetype(config.font_path, font_style.size)
        box = font.getbbox(an2cn(value))
        h, w = abs(box[1] - box[3]), abs(box[0] - box[2])
        pos = font_style.pos
        draw.text(
            (pos[0] - w / 2, pos[1] - h / 2),
            an2cn(value),
            font=font,
            fill=font_style.fill_color,
        )
    word = get_word()
    if word is not None:
        font = ImageFont.truetype(config.font_path, config.word_style.size)
        draw.text(
            config.word_style.pos,
            word,
            font=font,
            fill=config.word_style.fill_color,
            align="center",
        )
    image.save(config.cache_path)
    return config.cache_path
