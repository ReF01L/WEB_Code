from django.conf import settings
from django.db import models

from account.post import Position, PostCode


class Cell(models.Model):
    STATUSES = [(x, y) for x, y in zip(('Wait', 'Accepted', 'Declined'), (0, 1, -1))]
    date = models.DateField()
    vacancy = models.CharField(choices=((x.name, x.value) for x in Position), max_length=35)
    post_code = models.CharField(choices=((x.name, x.value) for x in PostCode), max_length=8)
    status = models.CharField(choices=STATUSES, max_length=10, default=STATUSES[0])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=35)
    post_code = models.CharField(max_length=8)
    vacancy = models.ManyToManyField(Cell, blank=True)
