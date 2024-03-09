import os
import logging
import logging.handlers

from pathlib import Path
from .config import get_config

config = get_config()
log_path = Path(config.log_path)

logger = logging.getLogger("logger")

stream_handler = logging.StreamHandler()

if not os.path.exists(log_path.parent):
    os.mkdir(log_path.parent)
if not os.path.exists(log_path):
    f = open(log_path, "x", encoding="utf-8")
    f.close()
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=config.log_path, when="midnight", interval=1, backupCount=7
)

logger.setLevel(logging.DEBUG)

stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.WARNING)

stream_format_pattern = logging.Formatter(
    fmt="%(asctime)s|%(levelname)s|%(name)s|%(filename)s:%(lineno)d|%(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

file_format_pattern = logging.Formatter(
    fmt="%(asctime)s|%(levelname)s|%(name)s|%(filename)s:%(lineno)d|%(message)s",
)

stream_handler.setFormatter(stream_format_pattern)
file_handler.setFormatter(file_format_pattern)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
