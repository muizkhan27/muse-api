# pylint: disable=missing-module-docstring
from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    '''
    This is a class for managing creation of different types of users.
    '''

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                if password:
                    user.set_password(password)
                else:
                    user.set_unusable_password()
                user.save(using=self._db)
                return user
        except Exception as exp:
            raise exp

    def create_admin(self, email, password=None, **extra_fields):
        '''
        Takes in email, password and extra attributes, creates a admin user and returns its object.
        '''
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''
        Takes in email, password and extra attributes, creates a super user and returns its object.
        '''
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password=password, **extra_fields)
