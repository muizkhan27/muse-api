from django.db import models
from django.contrib.auth.hashers import make_password


class Tenant(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False, default='')
    email = models.EmailField(max_length=100, null=True, blank=False, unique=True)
    password = models.CharField(max_length=100, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    subdomain = models.CharField(max_length=100, default='', unique=True)

    class Meta:
        db_table = 'tenants'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Tenant, self).save(*args, **kwargs)
