import os
from datetime import datetime
from arq.connections import RedisSettings
from arq import Worker
from httpx import AsyncClient
from logs import init_logging
from repository.Users import UsersRepository


logger = init_logging('worker')
redis_url = os.environ.get('REDIS_URL')
TIMEOUT_SECS_HTTX_CLIENT = 30


async def startup(ctx: Worker) -> None:
    logger.info("Worker Started")
    ctx['session'] = AsyncClient(timeout=TIMEOUT_SECS_HTTX_CLIENT)
    ctx['users_repository'] = UsersRepository()


async def shutdown(ctx: Worker) -> None:
    logger.info("Worker end")
    await ctx['session'].aclose()
    ctx['users_repository'].shutdown()


async def heavy_endpoint(ctx: Worker, random_value: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{random_value}] [{now}] Calling heavy endpoint...")
    # Busco simular llamado a un endpoint que me TARDE MUCHISIMO
    # en responder. En este caso, 10 segs.
    # (mismo puede ser un llamado LENTO a una base de datos, etc.)
    secs_delay = 10
    session: AsyncClient = ctx['session']
    url = 'https://httpbin.org/delay/%s' % secs_delay
    response = await session.get(url)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'[{random_value}] [{now}] Succesfuly called'
                f' heavy endpoint. Response: {response.json()}')

    # Tambien podemos acceder a la capa de repositorio...
    # (aquí es donde habría que consultar al CRUD de Alarmas,
    #  buscar si en el minuto actual hay alguna alarma
    #  de algún usuario, y si la hay, enviar una notificación)
    user_repository: UsersRepository = ctx['users_repository']
    user_id_one = user_repository.get_user(1)
    logger.info(f"[{random_value}] [{now}] User 1: {user_id_one}")


class WorkerSettings:
    functions = [heavy_endpoint]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(redis_url)
    handle_signals = False
