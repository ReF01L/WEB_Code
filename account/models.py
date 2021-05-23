from django.conf import settings
from django.db import models

from account.post import Position, PostCode


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=35)
    post_code = models.CharField(max_length=8)


class Cell(models.Model):
    date = models.DateField()
    vacancy = models.CharField(choices=((x.name, x.value) for x in Position), max_length=35)
    post_code = models.CharField(choices=((x.name, x.value) for x in PostCode), max_length=8)
