import asyncio
import os
from datetime import datetime
import random
from arq import create_pool
from arq.connections import RedisSettings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logs import init_logging


async def tick():
    now = datetime.now()
    id_device = random.randint(0, 99999)
    logger.info(f"[{id_device} {now}] Tock! Enqueuing job")
    await redis.enqueue_job('heavy_endpoint', id_device)
    logger.info(f"[{id_device} {now}] Job enqueued")

if __name__ == '__main__':
    logger = init_logging('clock')
    INTERVAL_SCHEDULE_SECS = int(os.environ.get('INTERVAL_SCHEDULE_SECS', 5))
    logger.info('Starting scheduler with interval %s' % INTERVAL_SCHEDULE_SECS)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=INTERVAL_SCHEDULE_SECS)
    scheduler.start()
    redis_url = os.environ.get('REDIS_URL')
    redis = asyncio.get_event_loop() \
        .run_until_complete(create_pool(RedisSettings.from_dsn(redis_url)))

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
