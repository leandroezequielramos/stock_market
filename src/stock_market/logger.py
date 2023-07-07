"""Logging functions to be used across the project."""

import logging
import sys

from uvicorn.logging import DefaultFormatter

from stock_market.settings import settings

FORMATTER = DefaultFormatter(
    "%(levelprefix)s %(name)s, line %(lineno)d — %(message)s"
)


def get_console_handler() -> logging.Handler:
    """Get a handler that logs to stdout.

    Returns:
        logging.Handler: A configured console handler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_logger(logger_name: str) -> logging.Logger:
    """Get a configured logger.

    Should be used with `__name__`

    Args:
        logger_name (str): The logger name

    Returns:
        logging.Logger: A configured logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(settings.LOGLEVEL.value)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger
