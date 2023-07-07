"""Logging functions to be used across the project."""

import logging
import sys

from uvicorn.logging import DefaultFormatter

from stock_market.settings import settings

FORMATTER = DefaultFormatter(
    "%(levelprefix)s %(name)s, line %(lineno)d — %(message)s"
)


def get_console_handler() -> logging.Handler:
    """
    gets logger console handler

    Returns
    -------
    logging.Handler
        logger console handler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_logger(logger_name: str) -> logging.Logger:
    """
    gets a logger instance

    Parameters
    ----------
    logger_name : str
        name to print in logging

    Returns
    -------
    logging.Logger
        logger built
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(settings.LOGLEVEL.value)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger
