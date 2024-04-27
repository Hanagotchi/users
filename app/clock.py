import os
import logging
import redis
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue

sched = BlockingScheduler()

# DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger("clock")
logging_level = os.environ.get("LOGGING_LEVEL", "DEBUG")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging_level,
    datefmt='%Y-%m-%d %H:%M:%S',
)
redis_url = os.getenv('REDIS_URL')

conn = redis.from_url(redis_url)
q = Queue(connection=conn)


def heavy_endpoint():
    logger.info('This job is very heavy ....')
    # sleep 3 min
    import time
    time.sleep(180)
    return "jaja, termineeeee xddxdx pusheado a firebase!!!!"


@sched.scheduled_job('interval', minutes=1)
def timed_job2():
    logger.info('This job is run every one minute.')
    q.enqueue(heavy_endpoint, 'heavy_endpoint')
    logger.info('Job enqueued, bye...')


logger.info('Ready to start the scheduler...')
sched.start()
