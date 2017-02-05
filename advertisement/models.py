# coding=utf-8
from __future__ import unicode_literals
from django.db import models


class Banner(models.Model):
    class Meta:
        verbose_name = u'Баннер'
        verbose_name_plural = u'Баннеры'

    image = models.ImageField(upload_to='banners', verbose_name=u'Картинка баннера')
    url = models.CharField(max_length=255, verbose_name=u'Ссылка', blank=True)
    description = models.CharField(max_length=255, verbose_name=u'Описание', blank=True)

