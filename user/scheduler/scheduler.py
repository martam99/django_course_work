from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
import sys
from user.models import Mailing
from user.services import send_mailing


def my_job():
    mail = Mailing.objects.all()
    return send_mailing(mail)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    if Mailing.status:
        if Mailing.PERIODS == 'PERIOD_HOURLY':
            return scheduler.add_job(my_job, 'interval', hours=1, name='send_mailings', jobstore='default')
        elif Mailing.PERIODS == 'PERIOD_DAILY':
            return scheduler.add_job(my_job, 'interval', hours=24, name='send_mailings', jobstore='default')
        elif Mailing.PERIODS == 'PERIOD_WEEKLY':
            return scheduler.add_job(my_job, 'interval', hours=168, name='send_mailings', jobstore='default')
        scheduler.start()
        print("Scheduler started...", file=sys.stdout)
    elif Mailing.status is False:
        scheduler.pause()

    if Mailing.end_time == timezone.now():
        scheduler.pause_job(my_job())
