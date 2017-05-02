"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import time
import os
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())

def tick1():
    print('Tick2! The time is: %s' % datetime.now())

def tick2():
    print('Tick2! The time is: %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone=utc)

    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.add_job(tick1, 'cron', id='my_test_job3', day_of_week='0-6', hour='4', minute='23')   #UTC时间
    scheduler.add_job(tick2, 'date', run_date=datetime(2017, 05, 02, 4, 23, 0))                     #UTC时间
    # trigger = CronTrigger(year='2009', month='2', hour='8-10', start_date='2009-02-03 11:00:00', timezone=timezone)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
