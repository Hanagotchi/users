from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minute.')


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

print('Ready to start the scheduler...')
sched.start()