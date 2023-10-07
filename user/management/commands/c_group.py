from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        g_manager = Group.objects.create(name='Managers')
        p1 = Permission.objects.get(codename='view_mailing')
        p2 = Permission.objects.get(codename='view_user')
        g_manager.permissions.add(p1, p2)
