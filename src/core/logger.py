import sys

from loguru import logger

from src.core.config import config

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format=config.logging.format,
)

logger.add(
    config.logging.file,
    format=config.logging.format,
)

osint_logger = logger.bind(service="osint")
