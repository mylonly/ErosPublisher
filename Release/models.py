from django.db import models
from App.models import App
from Package.models import Package
from Device.models import Device
import random

# Create your models here.
class Record(models.Model):
  appName = models.CharField(max_length=100)
  jsVersion = models.CharField(max_length=20, null=True)
  jsMD5 = models.CharField(max_length=100)
  appPlatform = models.CharField(max_length=20)
  appVersion = models.CharField(max_length=20)
  isDiff = models.BooleanField(default=True)
  deviceToken = models.CharField(max_length=100, unique=True)
  deviceName = models.CharField(max_length=50, null=True)
  osVersion = models.CharField(max_length=50, null=True)
  updateJSVersion = models.CharField(max_length=50, null=True)
  updateTime = models.DateTimeField(auto_now=True)
  ip = models.CharField(max_length=100)
  area = models.CharField(max_length=100, null=True)
  memo = models.CharField(max_length=100, null=True) #备注

  @classmethod
  def getiOSUpdateProcess(cls,iOSVersion,appName,jsVersion):
    total = Record.objects.filter(appPlatform='iOS', appVersion=iOSVersion, appName=appName)
    updated = total.filter(jsVersion=jsVersion)
    return (len(updated), len(total))

  @classmethod
  def getAndroidUpdateProcess(cls,AndroidVersion, appName, jsVersion):
    total = Record.objects.filter(appPlatform='Android', appVersion=AndroidVersion, appName=appName)
    updated = total.filter(jsVersion=jsVersion)
    return (len(updated), len(total))

  @classmethod
  def getTestUpdateProcess(cls, devices,jsVersion):
    total = Record.objects.filter(deviceToken_in=devices)
    updated = total.filter(jsVersion=jsVersion)
    return (len(updated), len(total))

  

class Release(models.Model):

  FILTER_TYPE = [
    (0, '灰度值'),
    (1, '指定设备'),
  ]

  appName = models.CharField(max_length=100)
  jsVersion = models.CharField(max_length=100)
  android = models.CharField(max_length=100)
  iOS = models.CharField(max_length=100)
  showUpdateAlert = models.BooleanField(default=False) #是否显示更新提示
  isForceUpdate = models.BooleanField(default=False) #是否强制更新
  changelog = models.CharField(max_length=500, null=True)
  filterType = models.IntegerField(choices=FILTER_TYPE, default=0)
  grayScale = models.FloatField(null=True)  #灰度值
  deviceIDs = models.CharField(max_length=5000, null=True, blank=True)
  createtime = models.DateTimeField(auto_now=True)

  @classmethod
  def gotHit(cls, data):
    appName = data.get('appName')
    appPlatform = data.get('appPlatform')
    appVersion = data.get('appVersion')
    deviceToken = data.get('deviceToken')
    releases = None
    if appPlatform == 'iOS' or appPlatform == 'ios':
      releases = Release.objects.filter(appName=appName, iOS=appVersion).order_by('-createtime')
    elif appPlatform == 'Android' or appPlatform == 'android':
      releases = Release.objects.filter(appName=appName, android=appVersion).order_by('-createtime')
    else:
      return None
    for release in releases:
      if release.filterType == 0: #按灰度值来决定是否匹配
        ##TODO: 判断当前的更新率是否已经达到灰度值，如果达到，不再掷骰子
        (iOS_updated, iOS_total) = Record.getiOSUpdateProcess(release.iOS,release.appName,release.jsVersion)
        (Android_updated, Android_total) = Record.getAndroidUpdateProcess(release.android, release.appName, release.jsVersion)
        total = iOS_total + Android_total
        updated = iOS_updated + Android_updated
        process = 0
        if total > 0:
          process = float(updated/total)
        if process < release.grayScale:
          randomGrayscale = random.random()
          if randomGrayscale <= release.grayScale:
            return release
      elif release.filterType == 1: #根据指定设备来匹配
        if release.deviceIDs.find(deviceToken) != -1:
          return release      
      else:
        continue
    return None
