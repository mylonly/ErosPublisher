from django.db import models
from App.models import App
# Create your models here.

class Package(models.Model):
  appName = models.CharField(max_length=100)
  jsVersion = models.CharField(max_length=20)
  android = models.CharField(max_length=20,null=True)
  ios = models.CharField(max_length=20,null=True)
  timestamp = models.BigIntegerField()
  jsPath = models.URLField(null=True)
  isForceUpdate = models.BooleanField(default=False)
  changelog = models.CharField(max_length=500, null=True)
  published = models.BooleanField(default=False) ##是否已发布

