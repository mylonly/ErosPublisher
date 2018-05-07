from django.db import models
from App.models import App
from Package.models import Package
from Device.models import Device

# Create your models here.
class Record(models.Model):
  appName = models.CharField(max_length=100)
  jsVersion = models.CharField(max_length=20)
  iOS = models.CharField(max_length=20, null=True)
  android = models.CharField(max_length=20, null=True)
  isDiff = models.BooleanField(default=True)
  deviceToken = models.CharField(max_length=100)
  deviceName = models.CharField(max_length=50, null=True)
  osVersion = models.CharField(max_length=50, null=True)
  updateJSVersion = models.CharField(max_length=50, null=True)