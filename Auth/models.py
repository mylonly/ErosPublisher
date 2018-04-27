from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser




class UserProfile(AbstractUser):

  ROLES = [
    ('admin',"管理员"),
    ('normal',"普通用户"),
    ('guest',"访客")
  ]

  avatar = models.URLField(max_length=500,default="https://pic.mylonly.com/2018-04-27-060452.jpg")
  role =  models.CharField(choices=ROLES, default='normal', max_length=10)

  REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['avatar', 'role']