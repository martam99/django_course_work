from smtplib import SMTPException

from django.core.mail import send_mail

from config import settings
from user.models import Logs


def send_mailing(subject, body, client, mail):
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client],
            fail_silently=False
        )
        Logs.objects.create(
            status=True,
            client=mail.client,
            mailing=mail.subject,
            mailings=mail
        )
    except SMTPException as err:
        Logs.objects.create(
            status=False,
            client=mail.client,
            mailing=mail.subject,
            mailings=mail,
            error_msg=err
        )

