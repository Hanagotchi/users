import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from users.app import heavy_endpoint
from worker import conn

sched = BlockingScheduler()

# DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger("clock")
logging_level = os.environ.get("LOGGING_LEVEL", "DEBUG")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging_level,
    datefmt='%Y-%m-%d %H:%M:%S',
)
q = Queue(connection=conn)


@sched.scheduled_job('interval', minutes=1)
def timed_job2():
    logger.info('This job is run every one minute.')
    q.enqueue(heavy_endpoint, 'heavy_endpoint')
    logger.info('Job enqueued, bye...')


logger.info('Ready to start the scheduler...')
sched.start()
