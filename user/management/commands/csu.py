import os
from dotenv import load_dotenv
from django.core.management import BaseCommand

from config.settings import BASE_DIR
from user.models import User

load_dotenv(BASE_DIR / '.env')


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv("email"),
            first_name=os.getenv("first_name"),
            last_name=os.getenv("last_name"),
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(os.getenv('password'))
        user.save()
