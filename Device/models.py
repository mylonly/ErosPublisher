from django.db import models

# Create your models here.
class Device(models.Model):
  PLATFORMS = [
    ('Android', '安卓'),
    ('iOS', 'iOS')
  ]
  device_name = models.CharField(max_length=100)
  device_token = models.CharField(max_length=50)
  os_name = models.CharField(max_length=20, choices=PLATFORMS)
  os_version = models.CharField(max_length=100)
