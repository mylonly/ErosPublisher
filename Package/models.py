from django.db import models

# Create your models here.


class Package(models.Model):
  name = models.CharField(max_length=100)
  version = models.CharField(max_length=20)
  android = models.CharField(max_length=20)
  ios = models.CharField(max_length=20)
  jsPath = models.URLField(null=True)
  isForceUpdate = models.BooleanField(default=False)
  changelog = models.CharField(max_length=500, null=True)
