# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import models
from django.conf import settings


class AccountUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email, is_active=True,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = AccountUserManager()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_OTHERS = 3
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHERS, _("Others")),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=10, unique=True)
    avatar = models.ImageField(
        upload_to="images/users/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url
    # return self.avatar.url if self.avatar else static('assets/images/default-profile-picture.png')


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    house_number_name = models.CharField(
        "House number/name", max_length=40, null=True)
    street = models.CharField(max_length=40, null=True, blank=True)
    town = models.CharField(max_length=40, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
