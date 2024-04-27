
# https://python-rq.org/patterns/
import os
import logging
import redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker


logger = logging.getLogger("worker")
logging_level = os.environ.get("LOGGING_LEVEL", "DEBUG")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging_level,
    datefmt='%Y-%m-%d %H:%M:%S',
)

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        queue = Queue(connection=conn)
        logger.info('Queue elements:', queue.count)
        queue.empty()
        logger.info('Queue elements:', queue.count)
        worker = Worker(map(Queue, listen))
        worker.clean_registries()
        logger.info('Ready to start the worker...')
        worker.work()
