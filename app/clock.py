import asyncio
import os
from datetime import datetime
from arq import create_pool
from arq.connections import RedisSettings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logs import init_logging


async def tick():
    now = datetime.now()
    logger.info('Tick! Prepare to enqueue job at: %s' % now)
    await redis.enqueue_job('heavy_endpoint', 'FEDE time % s' % now)
    logger.info('Tock! Enqueued job at: %s' % datetime.now())

INTERVAL_SCHEDULE_SECS = 60


if __name__ == '__main__':
    logger = init_logging('clock')
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
