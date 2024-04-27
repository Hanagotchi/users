import asyncio
from datetime import datetime
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


async def async_heavy_endpoint(id_device: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{time}] Async RQ test: The param is: {id_device}")
    await asyncio.sleep(30)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{time}] Async RQ test: The param is: {id_device}")


def heavy_endpoint(id_device: str):
    logger.info(f'Heavy endpoint started for device {id_device}')
    # sleep 3 min
    import time
    time.sleep(30)
    result = "jaja, termineeeee XDDXDXDXDXDXDXDX pusheado a firebase!!!!"
    logger.info(f'Heavy endpoint finished for device {id_device}')
    return result


def async_heavy_endpoint_wrapper(*args, **kwargs):
    loop = asyncio.get_event_loop()
    coro = async_heavy_endpoint(*args, **kwargs)
    loop.create_task(coro)
