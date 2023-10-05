from django.db import models
from .user import User


class UserTaxInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tax_year = models.IntegerField(null=False)
    tax_info = models.JSONField(blank=False)
    tax_plan = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'user_tax_info'
        unique_together = ('user', 'tax_year')

    def __str__(self):
        return self.tax_info
