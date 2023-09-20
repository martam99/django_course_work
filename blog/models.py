from datetime import datetime

from django.db import models


# В сущность блога добавьте следующие поля:
#
# заголовок,
# содержимое статьи,
# изображение,
# количество просмотров,
# дата публикации.


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название блога')
    body = models.TextField(verbose_name='Содержимое блога')
    published_date = models.DateTimeField(verbose_name='дата публикации.', default=datetime.now)
    view_count = models.IntegerField(default=0, verbose_name='количество просмотров.')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение.')

    def __str__(self):
        return f'{self.title} {self.body}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


