from smtplib import SMTPException

from django.core.mail import send_mail

from config import settings
from user.models import Mailing, Logs


def send_mailing():
    mail = Mailing.objects.all()
    try:
        send_mail(
            subject=mail.subject,
            message=mail.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mail.client],
            fail_silently=False
        )
        log = Logs.objects.create(
            status=True,
            client=mail.client,
            mailing=mail.subject,
            mailings=mail
        )
        return log
    except SMTPException as err:
        log = Logs.objects.create(
            status=False,
            client=mail.client,
            mailing=mail.subject,
            mailings=mail,
            error_msg=err
        )
        return log

