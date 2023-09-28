from django.core.management import BaseCommand

from user.mail_creation import send_mailing

mailing = send_mailing()


class Command(BaseCommand):
    def handle(self, *args, **options):
        return mailing
