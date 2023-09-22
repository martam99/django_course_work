import datetime as dt
import time

import schedule
from scheduler import Scheduler
from scheduler.trigger import Monday

from user.models import Mailing
from user.views import MailCreateView


def my_job():
    return MailCreateView.form_valid


my_schedule = Scheduler()


def start_job():
    if Mailing.STATUSES == 'STATUS_STARTED':
        if Mailing.PERIODS == 'PERIOD_HOURLY':
            return my_schedule.hourly(dt.time(minute=30, second=15), my_job())
        if Mailing.PERIODS == 'PERIOD_DAILY':
            return my_schedule.daily(dt.time(hour=16, minute=30), my_job())
        elif Mailing.PERIODS == 'PERIOD_WEEKLY':
            return my_schedule.weekly(Monday(dt.time(hour=16, minute=30)), my_job())
    elif Mailing.STATUSES == 'STATUS_DONE':
        my_schedule.delete_jobs()
        return 'Stopped'

    while True:
        my_schedule.exec_jobs()
        time.sleep(1)
