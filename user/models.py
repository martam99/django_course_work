import traceback
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.models import Blog
from config import settings
from user.views import MailCreateView

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.CharField(max_length=150, verbose_name='почта', unique=True)
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    avatar = models.ImageField(upload_to='user/', verbose_name='фото', default='no avatar')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Блог')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Client(models.Model):
    fullname = models.CharField(max_length=150, verbose_name='ФИО', **NULLABLE)
    mail = models.EmailField(max_length=150, verbose_name='Почта', unique=True)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'client'


class Mailing(models.Model):
    PERIOD_HOURLY = 'hourly'
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'

    PERIODS = (
        (PERIOD_HOURLY, 'Раз в час'),
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),

        (STATUS_DONE, 'Завершена'),
    )

    published_time = models.DateTimeField(verbose_name='время', default=datetime.now())
    period = models.CharField(max_length=20, verbose_name='период', choices=PERIODS)
    status = models.CharField(max_length=20, verbose_name='статус', choices=STATUSES)
    subject = models.CharField(max_length=200, verbose_name='тема письма', default='Без темы')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Пользователь')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Клиент')

    def __str__(self):
        return f'{self.subject}'


class Logs(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус'),
    date_end = models.DateTimeField(verbose_name='дата и время последней попытки'),
    client = models.EmailField(max_length=150, verbose_name='Почта клиента')
    mailing = models.CharField(max_length=150, verbose_name='Рассылка, которая отправлялась')
    error_msg = models.TextField(verbose_name='Ответ сервера')
    mailings = models.OneToOneField(Mailing, on_delete=models.CASCADE)

    # @property
    # def statuses(self):
    #     if MailCreateView.form_valid is True:
    #         return 'Успешно'
    #
    # @property
    # def date(self):
    #     return Mailing.objects.all().order_by("published_time").last()
    #
    # @property
    # def clients(self):
    #     return Mailing.objects.all().order_by('client')
    #
    # @property
    # def mail(self):
    #     return Mailing.objects.all().order_by('subject')
    #
    # @property
    # def error(self):
    #     if MailCreateView.form_valid == 'SMTPException':
    #         return 'Ошибка:\n', traceback.format_exc()
    #     else:
    #         return 'Успешно'


