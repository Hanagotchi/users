import asyncio
import os
from datetime import datetime
from arq.connections import RedisSettings
from arq import Worker
from httpx import AsyncClient
from logs import init_logging


logger = init_logging('worker')
redis_url = os.environ.get('REDIS_URL')


async def startup(ctx: Worker) -> None:
    logger.info("Worker Started")
    ctx['session'] = AsyncClient()


async def shutdown(ctx: Worker) -> None:
    logger.info("Worker end")
    await ctx['session'].aclose()


async def heavy_endpoint(ctx: Worker, id_user: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'[{time}] starting heavy endpoint for {id_user}')
    session: AsyncClient = ctx['session']
    url = 'https://hub.dummyapis.com/delay?seconds=15'
    response = await session.get(url)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'[{time}] response for {id_user}: {response.json()}')


class WorkerSettings:
    functions = [heavy_endpoint]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(redis_url)
    handle_signals = False
