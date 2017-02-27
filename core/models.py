# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'пользователи'

    email = models.EmailField(verbose_name=u'Email', unique=True)
    first_name = models.CharField(verbose_name=u'Имя', max_length=30)
    last_name = models.CharField(verbose_name=u'Фамилия', null=True, blank=True, max_length=60)
    phone = models.CharField(verbose_name=u'Номер телефона', max_length=60, blank=True)

    is_staff = models.BooleanField(verbose_name=u'Персонал?', default=False)
    is_active = models.BooleanField(verbose_name=u'Активен?', default=True)
    date_joined = models.DateTimeField(verbose_name=u'Дата регистрации', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return ' '.join(parts)

    def get_short_name(self):
        return '{0}'.format(self.email)

    def __unicode__(self):
        return '{0}'.format(self.email)
