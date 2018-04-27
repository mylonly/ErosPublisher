from django.db import models

# Create your models here.

class App(models.Model):
  name = models.CharField(max_length=100)
  intro = models.CharField(max_length=500)
  logo = models.URLField(null=True)
  