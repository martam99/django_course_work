from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=input('Введите почту пользователя: '),
            first_name=input('Введите имя пользователя: '),
            last_name=input('Введите фамилию пользователя: '),
            is_staff=True,
            is_active=True,
        )

        user.set_password(input('Создайте пароль: '))
        user.save()
        managers = Group.objects.get(name='Managers')
        managers.user_set.add(user)
