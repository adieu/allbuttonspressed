from . import api
from django.db import models

class URLRoute(models.Model):
    url = models.CharField(primary_key=True, max_length=256)
    handler = models.CharField(max_length=64)
    target = models.CharField(max_length=64, null=True)
