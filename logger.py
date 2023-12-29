import sys
import os
import logging
import datetime

from logging import RootLogger, StreamHandler, Formatter, FileHandler


def startLogging() -> RootLogger:
    if not os.path.exists("logs"):
        os.makedirs("logs")

    current_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    logger: RootLogger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_handler: StreamHandler = logging.StreamHandler(sys.stdout)
    console_formatter: Formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)

    file_handler: FileHandler = logging.FileHandler(
        f"logs/{current_time}_bot.log", mode="w"
    )
    file_formatter: Formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
