from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from blog.models import Blog
from django.conf import settings

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.CharField(max_length=150, verbose_name='почта', unique=True)
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    avatar = models.ImageField(upload_to='user/', verbose_name='фото', default='no avatar')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Блог')
    is_active = models.BooleanField(default=True, verbose_name='activity')

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Client(models.Model):
    fullname = models.CharField(max_length=150, verbose_name='ФИО', **NULLABLE)
    mail = models.EmailField(max_length=150, verbose_name='Почта', unique=True)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    objects = models.Manager()

    def __str__(self):
        return f'{self.mail}'

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

    published_time = models.DateTimeField(verbose_name='время создания рассылки', default=datetime.now())
    end_time = models.DateTimeField(verbose_name='время окончания рассылки в формате «Д.М.Г Ч:М:С»', **NULLABLE)
    period = models.CharField(max_length=20, verbose_name='период', choices=PERIODS)
    status = models.BooleanField(max_length=20, verbose_name='Запустить', default=False)
    subject = models.CharField(max_length=200, verbose_name='тема письма', default='Без темы')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Пользователь')
    client = models.ManyToManyField(Client, verbose_name='Клиент')

    objects = models.Manager()

    def __str__(self):
        return f'{self.subject}, {self.client}, {self.owner} {self.period}'


class Logs(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус', default='Успешно')
    date_end = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    client = models.EmailField(max_length=150, verbose_name='Почта клиента', **NULLABLE)
    mailing = models.CharField(max_length=150, verbose_name='Рассылка, которая отправлялась', **NULLABLE)
    error_msg = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f'{self.status} {self.client} {self.mailing} {self.error_msg}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
