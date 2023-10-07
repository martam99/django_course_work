from smtplib import SMTPException
from django.core.mail import send_mail
from user.models import Logs
from django.conf import settings


def send_mailing(mailing):
    for client in mailing.client.all():
        try:
            send_mail(
                subject=mailing.subject,
                message=mailing.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client],
                fail_silently=False
            )
            log = Logs.objects.create(
                status=True,
                client=client.mail,
                mailing=mailing.subject,
                mailings=mailing,
                date_end=mailing.published_time
            )
            log.save()
            return log
        except SMTPException as err:
            log = Logs.objects.create(
                status=False,
                client=client.mail,
                mailing=mailing.subject,
                mailings=mailing,
                date_end=mailing.published_time,
                error_msg=err
            )
            log.save()
            return log
