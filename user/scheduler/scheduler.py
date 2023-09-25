from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys

from user.models import Mailing
from user.views import MailCreateView


def my_job():
    return MailCreateView.form_valid


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    if Mailing.STATUSES == 'STATUS_STARTED':
        if Mailing.PERIODS == 'PERIOD_HOURLY':
            return scheduler.add_job(my_job, 'interval', hours=1,  name='send_mailings', jobstore='default')
        elif Mailing.PERIODS == 'PERIOD_DAILY':
            return scheduler.add_job(my_job, 'interval', hours=24, name='send_mailings', jobstore='default')
        elif Mailing.PERIODS == 'PERIOD_WEEKLY':
            return scheduler.add_job(my_job, 'interval', hours=168, name='send_mailings', jobstore='default')
        scheduler.start()
        print("Scheduler started...", file=sys.stdout)
    elif Mailing.STATUSES == 'STATUS_DONE':
        scheduler.pause()
