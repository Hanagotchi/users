import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

logger = logging.getLogger("clock")
# DEBUG, INFO, WARNING, ERROR, CRITICAL
logging_level = os.environ.get("LOGGING_LEVEL", "DEBUG")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging_level,
    datefmt='%Y-%m-%d %H:%M:%S',
)


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    logger.info('This job is run every three minutes.')


@sched.scheduled_job('interval', minutes=1)
def timed_job2():
    logger.info('This job is run every one minute.')


logger.info('Ready to start the scheduler...')
sched.start()
