# coding=utf-8
from __future__ import unicode_literals

import random

from django.db import models


class AdvertManager(models.Manager):
    def get_showable(self):
        return self.get_queryset().filter(is_moderated=True, is_active=True, is_sold=False)

    def get_best_adverts(self):
        l = list(self.get_showable().filter(is_best=True))
        random.shuffle(l)
        return l[:2]


# Create your models here.
class Advert(models.Model):
    class Meta:
        verbose_name = u'Объявление'
        verbose_name_plural = u'Обявления'

    objects = AdvertManager()

    header = models.CharField(max_length=255, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст объявления')
    photo = models.ImageField(verbose_name=u'Фото объявления', null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=u'Город')
    address = models.CharField(max_length=250, verbose_name=u'Адрес')
    price = models.PositiveIntegerField(verbose_name=u'Цена')
    type = models.ForeignKey('adverts.SubCategory', verbose_name=u'Под категория')
    owner = models.ForeignKey('core.User', verbose_name=u'Владелец')

    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')

    is_moderated = models.BooleanField(default=False, verbose_name=u'Объявление проверено')
    is_active = models.BooleanField(default=True, verbose_name=u'Объявление активно')
    is_sold = models.BooleanField(default=False, verbose_name=u'Товар продан')
    is_best = models.BooleanField(default=False, verbose_name=u'Лучшее объявление (правый блок (проплачено))')

    def __unicode__(self):
        return (self.header + ' ' + self.text)[:150]


class Category(models.Model):
    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    name = models.CharField(max_length=255, verbose_name=u'Название категории')

    def __unicode__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        verbose_name = u'Подкатегория'
        verbose_name_plural = u'Подкатегории'

    name = models.CharField(max_length=255, verbose_name=u'Название подкатегории')
    category = models.ForeignKey('adverts.Category', verbose_name=u'Категория')

    def __unicode__(self):
        return self.name
