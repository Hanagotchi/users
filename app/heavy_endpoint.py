import os
import logging


# DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger("heavy_endpoint")
logging_level = os.environ.get("LOGGING_LEVEL", "DEBUG")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging_level,
    datefmt='%Y-%m-%d %H:%M:%S',
)


def heavy_endpoint(id_device: str):
    logger.info(f'Heavy endpoint started for device {id_device}')
    # sleep 3 min
    import time
    time.sleep(180)
    return "jaja, termineeeee XDDXDXDXDXDXDXDX pusheado a firebase!!!!"
