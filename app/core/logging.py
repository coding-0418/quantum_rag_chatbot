import sys

from loguru import logger

from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level, backtrace=False, diagnose=False)


__all__ = ["logger", "configure_logging"]
