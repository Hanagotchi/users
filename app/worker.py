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
    # session: AsyncClient = ctx['session']
    # fb = 'https://facebook.com'
    # response = await session.get(fb)
    # print(f'[{time}] {fb}: {response.text:.80}...')
    print(f'[{time}] sleep startesd for {id_user}')
    await asyncio.sleep(30)
    print(f'[{time}] sleep finished for {id_user}')


class WorkerSettings:
    functions = [heavy_endpoint]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(redis_url)
    handle_signals = False
