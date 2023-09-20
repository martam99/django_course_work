import time
import schedule as schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from user.models import Mailing
from user.views import MailCreateView


def my_job():
    return MailCreateView.form_valid


scheduler = BackgroundScheduler()
scheduler.add_job(my_job, CronTrigger(second='0'))
if Mailing.PERIODS == 'PERIOD_HOURLY':
    schedule.every().hour.do(my_job)
if Mailing.PERIODS == 'PERIOD_DAILY':
    schedule.every().day.at("17:00").do(my_job)
elif Mailing.PERIODS == 'PERIOD_WEEKLY':
    schedule.every().monday.at("17:00").do(my_job)

while True:
    schedule.run_pending()
    time.sleep(1)

    scheduler.start()
    print("Scheduler started")
