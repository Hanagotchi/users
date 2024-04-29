import os
import asyncio
from arq import Worker
from logs import init_logging
from httpx import AsyncClient
from datetime import datetime
from arq.connections import RedisSettings
from repository.Users import UsersRepository

logger = init_logging('worker')
redis_url = os.environ.get('REDIS_URL')
TIMEOUT_SECS_HTTPX_CLIENT = 30


async def send_notification(ctx: Worker,
                            device_token: str,
                            content: str,
                            date_time: datetime):
    logger.info(f"Sending alarm notification to "
                f"{device_token} with content: {content} at {date_time}")
    # este es un ejemplo usando httpx para hacer un request a un endpoint
    # de forma asincrona,
    # simulando que es un request a firebase para enviar una notificacion

    secs_delay = 1
    random_value = int(datetime.now().timestamp())
    session: AsyncClient = ctx['session']
    url = 'https://httpbin.org/delay/%s' % secs_delay
    response = await session.get(url)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'[{random_value}] [{now}] Succesfuly called'
                f' firebase endpoint. Response: {response.json()}')

    # buscar que el endpoint de firebase para enviar notificaciones
    # sea ASYNC, asi no bloquea el worker y se logra aprovechar
    # el envio de notificaciones en paralelo con la programacion asincrona
    #
    # ...si hubiera que hacerlo sincrono, el llamado a firebase
    # terminaria siendo secuencial para N notificaciones, y no es eficiente...


async def alarm_manager(ctx: Worker, date_time: datetime):
    try:
        logger.debug(f"Checking alarms for {date_time}")
        user_repository: UsersRepository = ctx['users_repository']
        result = user_repository.get_users_to_notify(date_time)
        if len(result) == 0:
            logger.debug(f"No alarms to notify at {date_time}")
            return
        tasks = []
        logger.info(f"Found {len(result)} alarms to notify at {date_time}")
        for (id, content, device_token) in result:
            if device_token is None:
                logger.debug(f"Alarm with id {id} has no device_token. "
                             f"Skipping...")
                continue
            logger.debug(f"Preparing task to send notification to "
                         f"{device_token} with content: "
                         f"{content} at {date_time}")
            task = asyncio.create_task(send_notification(ctx,
                                                         device_token,
                                                         content,
                                                         date_time))
            tasks.append(task)

        logger.debug("Wating for all tasks to finish...")
        await asyncio.gather(*tasks)
        logger.info(f"All alarms notified at {date_time}")
    except Exception as e:
        logger.error(f"Error while processing alarms on {date_time}. "
                     f"Detail: {e}")
        # NO raise e, porque sino el worker se cae y no se procesan
        # los proximos eventos de alarma

        # lo ideal seria enviar informacion del error a un sistema de
        # monitoreo para que se pueda analizar y corregir el posible bug
        pass


async def startup(ctx: Worker) -> None:
    logger.info("Worker Started")
    ctx['session'] = AsyncClient(timeout=TIMEOUT_SECS_HTTPX_CLIENT)
    ctx['users_repository'] = UsersRepository()


async def shutdown(ctx: Worker) -> None:
    logger.info("Worker end")
    await ctx['session'].aclose()
    ctx['users_repository'].shutdown()


class WorkerSettings:
    functions = [alarm_manager]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(redis_url)
    handle_signals = False
