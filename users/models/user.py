from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    '''
    This is a class for creating users.
    '''
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    first_name = None
    last_name = None
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
