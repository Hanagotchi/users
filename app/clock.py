import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from heavy_endpoint import async_heavy_endpoint_wrapper
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


@sched.scheduled_job('interval', minutes=0.10)
def timed_job2():
    logger.info('This job is run every .. seconds.')
    id_device = "pepito73"
    q.enqueue(async_heavy_endpoint_wrapper, id_device)
    logger.info('Job enqueued, bye...')


logger.info('Ready to start the scheduler...')
sched.start()
