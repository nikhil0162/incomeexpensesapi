from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from helpers.models import TimestampModel

User = get_user_model()


class Income(TimestampModel):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLES', 'SIDE-HUSTLES'),
        ('OTHERS', 'OTHERS')
    ]

    source = models.CharField(choices=SOURCE_OPTIONS,max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ('-date',)
        verbose_name = _('Income')
        verbose_name_plural = _('Income')

    def __str__(self):
        return f'{self.owner}\'s income'
