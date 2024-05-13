import os
import asyncio
import json

from arq import Worker
from logs import init_logging
from httpx import AsyncClient
from datetime import datetime
from arq.connections import RedisSettings
from repository.Users import UsersRepository
from async_firebase import AsyncFirebaseClient
from async_firebase import messages

logger = init_logging('worker')
redis_url = os.environ.get('REDIS_URL')
TIMEOUT_SECS_HTTPX_CLIENT = 30

client = AsyncFirebaseClient()
firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
parsed_credentials = json.loads(firebase_credentials)
client.creds_from_service_account_info(parsed_credentials)


async def send_notification(ctx: Worker,
                            device_token: str,
                            content: str,
                            date_time: datetime):
    logger.info(f"Sending alarm notification to "
                f"{device_token} with content: {content} at {date_time}")

    response = await client.\
        send(message=messages.Message(token=device_token,
                                      notification=messages.
                                      Notification(title="Recordatorio",
                                                   body=content)))
    logger.info(f"Notification sent to {device_token}")
    logger.debug(f"Response client.push: {response}")


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

        logger.debug("Waiting for all tasks to finish...")
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
