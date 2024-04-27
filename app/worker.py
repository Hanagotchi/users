import os
from datetime import datetime
from arq.connections import RedisSettings
from arq import Worker
from httpx import AsyncClient
from logs import init_logging


logger = init_logging('worker')
redis_url = os.environ.get('REDIS_URL')
TIMEOUT_SECS_HTTX_CLIENT = 30


async def startup(ctx: Worker) -> None:
    logger.info("Worker Started")
    ctx['session'] = AsyncClient(timeout=TIMEOUT_SECS_HTTX_CLIENT)


async def shutdown(ctx: Worker) -> None:
    logger.info("Worker end")
    await ctx['session'].aclose()


async def heavy_endpoint(ctx: Worker, id_device: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{id_device} {now}] Calling heavy endpoint...")
    session: AsyncClient = ctx['session']
    secs_delay = 10
    url = 'https://httpbin.org/delay/%s' % secs_delay
    response = await session.get(url)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'[{id_device} {now}] Succesfuly called'
                f' heavy endpoint. Response: {response.json()}')


class WorkerSettings:
    functions = [heavy_endpoint]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(redis_url)
    handle_signals = False
