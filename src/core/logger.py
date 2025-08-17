from loguru import logger
import sys
from src.core.config import logger_settings


def patch_record(record):
    record["extra"]["module"] = record["extra"].get("module", "no-module")


def setup_logger():
    logger.remove()
    logger.configure(patcher=patch_record)

    logger.add(
        sys.stdout,
        level=logger_settings.LOG_LEVEL.value,
        enqueue=True,
        format=lambda _: "\n<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{"
                         "name}</cyan>:<cyan>{"
                         "function}</cyan> - <level>{message}</level>"
    )

    logger.add(
        logger_settings.LOG_FILE_PATH,
        level=logger_settings.LOG_LEVEL.value,
        rotation=logger_settings.LOG_ROTATION,
        retention=logger_settings.LOG_RETENTION,
        compression=logger_settings.LOG_COMPRESSION,
        enqueue=True,
        backtrace=True,
        diagnose=False,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[module]} | {message}"
    )


def get_logger(module: str):
    return logger.bind(module=module)
