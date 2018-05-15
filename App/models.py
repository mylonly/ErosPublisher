from django.db import models

# Create your models here.

class App(models.Model):
  name = models.CharField(max_length=100)    #显示名称
  appName = models.CharField(max_length=100) #项目名称
  intro = models.CharField(max_length=500)
  logo = models.URLField(null=True)