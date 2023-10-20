import sys
import os
import logging
import datetime


def startLogging() -> None:
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_handler = logging.FileHandler(f"logs/{current_time}_bot.log", mode="w")

    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
