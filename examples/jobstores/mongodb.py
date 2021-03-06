"""
This example demonstrates the use of the MongoDB job store.
On each run, it adds a new alarm that fires after ten seconds.
You can exit the program, restart it and observe that any previous alarms that have not fired yet
are still active. Running the example with the --clear switch will remove any existing alarms.
"""

from datetime import datetime, timedelta
import sys
import os
from pytz import utc
from pymongo import MongoClient

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore

def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=utc)
    client = MongoClient('mongodb://127.0.0.1:27017/blusql')
    jobstore = MongoDBJobStore(client=client, database='blusql', collection='apscheduljobs')
    scheduler.add_jobstore(jobstore)
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        scheduler.remove_all_jobs()

    alarm_time = datetime.now() + timedelta(seconds=10) -timedelta(hours=8)
    scheduler.add_job(alarm, 'date', run_date=alarm_time, args=[datetime.now()])

    print('To clear the alarms, run this example with the --clear argument.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
