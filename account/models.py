from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=35)
    post_code = models.CharField(max_length=8)
