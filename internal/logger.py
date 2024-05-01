import os
import sys
import logging
import logging.handlers
from loguru import logger

from pathlib import Path
from .config import get_config

config = get_config()
log_path = Path(config.log_path)
logger.debug("加载logger中，logger文件目录：{path}", path=log_path)

default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)

logger.remove()
stout_logger_id = logger.add(sys.stdout, level=0, diagnose=False, format=default_format)
file_logger_id = logger.add(
    log_path, level=0, rotation="1 day", retention="1 week", delay=True
)
logger.debug("加载logger成功")

# logger = logging.getLogger("logger")

# stream_handler = logging.StreamHandler()

# if not os.path.exists(log_path.parent):
#     os.mkdir(log_path.parent)
# if not os.path.exists(log_path):
#     f = open(log_path, "x", encoding="utf-8")
#     f.close()
# file_handler = logging.handlers.TimedRotatingFileHandler(
#     filename=config.log_path, when="midnight", interval=1, backupCount=7,encoding='utf-8'
# )

# logger.setLevel(logging.DEBUG)

# stream_handler.setLevel(logging.DEBUG)
# file_handler.setLevel(logging.DEBUG)

# stream_format_pattern = logging.Formatter(
#     fmt="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s",
#     datefmt="%Y/%m/%d %H:%M:%S",
# )

# file_format_pattern = logging.Formatter(
#     fmt="%(asctime)s|%(levelname)s|%(name)s|%(filename)s:%(lineno)d|%(message)s",
# )

# stream_handler.setFormatter(stream_format_pattern)
# file_handler.setFormatter(file_format_pattern)

# logger.addHandler(stream_handler)
# logger.addHandler(file_handler)
