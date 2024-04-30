import os
import asyncio
from arq import create_pool
from logs import init_logging
from datetime import datetime
from arq.connections import RedisSettings
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def tick():
    date_time_to_check = datetime.now().replace(second=0, microsecond=0)
    logger.info(f"[Tick! Enqueuing job for {date_time_to_check}]")
    await redis.enqueue_job('alarm_manager', date_time_to_check)
    logger.info(f"[Tock! Job enqueued for {date_time_to_check}")

if __name__ == '__main__':
    logger = init_logging('clock')

    scheduler = AsyncIOScheduler()

    scheduler.add_job(tick,
                      'cron',
                      minute='0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55',
                      second='0')
    scheduler.start()

    redis_url = os.environ.get('REDIS_URL')
    redis = asyncio.get_event_loop() \
        .run_until_complete(create_pool(RedisSettings.from_dsn(redis_url)))

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
