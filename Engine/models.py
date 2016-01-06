from __future__ import unicode_literals

from django.db import models


# Create your models here.
class LatestFolderPath(models.Model):
    user_id = models.CharField(max_length=20)
    path = models.CharField(max_length=50)
