import logging
from typing import TypeVar, Optional

from backend.src.core.settings import LoggerSettings


LevelType = TypeVar('LevelType')


def setup_logger(
        name: str,
        level: LevelType,
        file_handler: Optional[logging.FileHandler],
        stream_handler: Optional[logging.StreamHandler]
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if file_handler not in logger.handlers:
        logger.addHandler(file_handler)

    if stream_handler not in logger.handlers:
        logger.addHandler(stream_handler)

    return logger


def setup_logger_file_handler(level: LevelType, file_name: str, settings: LoggerSettings = LoggerSettings()) -> logging.FileHandler:
    file_path = (settings.dir_path / f'{file_name}.log')
    handler = logging.FileHandler(file_path)
    handler.setFormatter(settings.formater)
    handler.setLevel(level)

    return handler


def setup_logger_stream_handler(level: LevelType, settings: LoggerSettings = LoggerSettings()) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setFormatter(settings.formater)
    handler.setLevel(level)

    return handler
