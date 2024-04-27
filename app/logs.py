import os
import logging
from logging import Logger


def init_logging(package_name: str) -> Logger:
    logger = logging.getLogger(package_name)
    logging_level = os.environ.get("LOGGING_LEVEL", "DEBUG")
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger.info(f"Logging level set to {logging_level}")
    return logger
