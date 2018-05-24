from django.shortcuts import render
from rest_framework import views,generics
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from App.models import App
from Device.models import Device
from Package.models import Package
from Release.models import Record, Release
from Release.serializers import RecrodSerializer, ReleaseSerializer, RecordFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.serializers import ValidationError
import bsdiff4
from ErosUpdate.settings import MEDIA_ROOT,MEDIA_URL
import os.path
import logging
from rest_framework.permissions import AllowAny
# Create your views here.

class RecordList(generics.ListAPIView):
  queryset = Record.objects.all()
  serializer_class = RecrodSerializer
  filter_backends = (DjangoFilterBackend,OrderingFilter)
  filter_fields = '__all__'
  ordering_fields = ('id', 'updatetime')
  filter_class = RecordFilter

  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return ErosResponse(data=response.data)

    serializer = self.get_serializer(queryset, many=True)
    return ErosResponse(data=serializer.data)


class QueryReleaseProgress(generics.GenericAPIView):
  def post(self, request, *args, **kwargs):
    appName = request.data.get('appName')
    iOS = request.data.get('iOS')
    android = request.data.get('android')
    jsVersion = request.data.get('jsVersion')
    if appName is None or iOS is None or android is None or jsVersion is None:
      return ErosResponse(status=ErosResponseStatus.PARAMS_ERROR, detail="params is missing, maybe is appName,iOS or android")
    
    iOS_Records = Record.objects.filter(appName=appName,appPlatform='iOS',appVersion=iOS)
    android_Records = Record.objects.filter(appName=appName, appPlatform='Android', appVersion=android)

    iOS_Updated_Records = Record.objects.filter(appName=appName,appPlatform='iOS',appVersion=iOS,jsVersion=jsVersion)
    android_Updated_Records = Record.objects.filter(appName=appName, appPlatform='Android', appVersion=android, jsVersion=jsVersion)


    resData = {
      'total':len(iOS_Records) + len(android_Records),
      'totalUpdated':len(iOS_Updated_Records) + len(android_Updated_Records),
      'iOS':len(iOS_Records),
      'iOSUpdated':len(iOS_Updated_Records),
      'Android':len(android_Records),
      "AndroidUpdate":len(android_Updated_Records)
    }
    return ErosResponse(data=resData)

class AddRelease(generics.CreateAPIView):
  serializer_class = ReleaseSerializer
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return ErosResponse(data=serializer.data)
    return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED,detail=serializer.errors)

class DeleteRelease(generics.GenericAPIView):
  def post(self, request, *args, **kwargs):
    ID = request.data.get("id")
    if ID is None:
      return ErosResponse(data=None, status=ErosResponseStatus.PARAMS_ERROR)
    else:
      try:
        release = Release.objects.get(id=ID)
        release.delete()
        return ErosResponse()
      except Release.DoesNotExist:
        return ErosResponse(status=ErosResponseStatus.NOT_FOUND)

class DeleteReleaseByPackage(generics.GenericAPIView):
  def post(self, request, *args, **kwargs):
      jsMD5 = request.data.get("jsMD5")
      if jsMD5 is None:
        return ErosResponse(data=None, status=ErosResponseStatus.PARAMS_ERROR)
      else:
        try:
          releases = Release.objects.filter(jsMD5=jsMD5)
          for release in releases:
            release.delete()
          return ErosResponse()
        except Release.DoesNotExist:
          return ErosResponse(status=ErosResponseStatus.NOT_FOUND)
          
class ReleaseUpdate(generics.GenericAPIView):
  serializer_class = ReleaseSerializer
  def post(self, request, *args, **kwargs):
    ID = request.data["id"]
    if ID is None:
      return ErosResponse(status=ErosResponseStatus.PARAMS_ERROR, detail="param [id] is missing...")
    try:
      instance = Release.objects.get(id=ID)
      partial = kwargs.pop('partial', False)
      serializer = self.get_serializer(instance, data=request.data, partial=partial)
      if serializer.is_valid():
         serializer.save()
         return ErosResponse(data=serializer.data)
      else:
        return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED, detail=serializer.errors)
      if getattr(instance, '_prefetched_objects_cache', None):
          # If 'prefetch_related' has been applied to a queryset, we need to
          # forcibly invalidate the prefetch cache on the instance.
          instance._prefetched_objects_cache = {}
    except Package.DoesNotExist:
      return ErosResponse(status=ErosResponseStatus.NOT_FOUND, detail="Release not found")

class ReleaseList(generics.ListAPIView):
  queryset = Release.objects.all()
  serializer_class = ReleaseSerializer
  filter_backends = (DjangoFilterBackend,OrderingFilter)
  filter_fields = ('appName','jsVersion') 
  ordering_fields = ('id', 'updatetime')
  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return ErosResponse(data=response.data)

    serializer = self.get_serializer(queryset, many=True)
    return ErosResponse(data=serializer.data) 

class CheckUpdate(generics.GenericAPIView):
  permission_classes = (AllowAny,)

  def get(self, requset, *args, **kwargs):
    return self.handleRequest(requset)
  def post(self, request, *args, **kwargs):
    return self.handleRequest(request)


  def handleRequest(self, requset):
    method = requset.method
    ip = requset.META.get('HTTP_X_FORWARDED_FOR')
    if ip is None:
      ip = requset.META.get('REMOTE_ADDR')

    requestData = None
    if method == 'GET':
      requestData = requset.query_params
    if method == 'POST':
      requestData = requset.data
    
    (validate,data) = self.validateData(requestData) 
    if not validate:
      return ErosResponse(status=ErosResponseStatus.PARAMS_ERROR)
    else:
      if data['deviceToken'] is None:
        data['deviceToken'] = ip
        data['ip'] = ip

    appName = data['appName']
    jsMD5 = data['jsMD5']
    oldPackages = Package.objects.filter(jsMD5=jsMD5)
    if len(oldPackages) > 0 :
      data['jsVersion'] = oldPackages[0].jsVersion
    release = Release.gotHit(data) #获取命中的更新包
    if not release:
      return ErosResponse(status=ErosResponseStatus.IS_LASTEST_PACKAGE)
    data['updateJSVersion'] = release.jsVersion
    

    self.updateRecord(data)  #更新记录

    try:
      package = Package.objects.get(appName=appName, jsVersion=release.jsVersion)
      newMD5 = package.jsMD5
      oldMD5 = data['jsMD5']
      isDiff = data['isDiff']
      jsPath = package.jsPath
      if newMD5 == oldMD5:
        return ErosResponse(status=ErosResponseStatus.IS_LASTEST_PACKAGE)
      if isDiff:
        (isDiff, jsPath) = self.diffPackage(oldMD5,newMD5,'http://'+requset.get_host()+MEDIA_URL)
      
      resData = {
          "diff":isDiff,
          "path":jsPath,
          "showUpdateAlert":release.showUpdateAlert,
          "isForceUpdate":release.isForceUpdate,
          "changelog":release.changelog,
      }
      return ErosResponse(data=resData)

    except Package.DoesNotExist:
      return ErosResponse(status=ErosResponseStatus.PACKAGE_NOT_FOUND, detail="jsVersion[%s] not found" % (jsVersion))

  def updateRecord(self, serializerData):
    deviceToken = serializerData.get('deviceToken')
    try:
      record = Record.objects.get(deviceToken=deviceToken)
      serializer= RecrodSerializer(record, data=serializerData)
      if serializer.is_valid():
        serializer.save()
      else:
        logger.error(str(serializer.erros))
    except Record.DoesNotExist:
      serializer = RecrodSerializer(data=serializerData)
      if serializer.is_valid():
        serializer.save()
      else:
        logger.error(str(serializer.erros))

  def validateData(self, requestData):
    appName = requestData.get('appName')
    jsMD5 = requestData.get('jsVersion')
    if jsMD5 is None:
      jsMD5 = requestData.get('jsMD5')
    appPlatform = requestData.get('appPlatform')
    appVersion = requestData.get('appVersion')
    if appPlatform is None:
      iOS = requestData.get('iOS')
      android = requestData.get('android')
      if iOS and android:
        appPlatform = None
      elif iOS:
        appPlatform = 'iOS'
        appVersion = iOS
      elif android:
        appPlatform = 'Android'
        appVersion = android
      else:
        appPlatform = None
    isDiff = requestData.get('isDiff')

    if appName and jsMD5 and appPlatform and appVersion and isDiff:
      validate_data = {
        'appName': appName,
        'jsMD5': jsMD5,
        'appPlatform': appPlatform,
        'appVersion': appVersion,
        'isDiff': isDiff,
        'deviceToken': requestData.get('deviceToken'),
        'deviceName': requestData.get('deviceName'),
        'osVersion': requestData.get('osVersion'),
        'ip': None,
        'updateJSVersion': None
      }
      return (True, validate_data)
    else:
      return (False,None)
  
  def diffPackage(self, oldMD5, newMD5, prefix):
    
    diffZipName = oldMD5+'-'+newMD5+'.zip'
    diffZipPath = MEDIA_ROOT+diffZipName

    oldZipName = oldMD5 + '.zip'
    oldZipPath = MEDIA_ROOT+oldZipName

    newZipName = newMD5 + '.zip'
    newZipPath = MEDIA_ROOT + newZipName

    #先判断diff文件存不存在,存在说明之前生成过这个增量包，直接返回
    exsit = os.path.isfile(diffZipPath) 
    if exsit:
      return (True,prefix+diffZipName)

    #判断老的js包存不存在，不存在返回最新全量包的地址
    exsit = os.path.isfile(oldZipPath) 
    if not exsit:
      return (False,prefix + newZipName)

    exsit = os.path.isfile(newZipPath)
    if not exsit:
      return (False,None)

    bsdiff4.file_diff(oldZipPath, newZipPath, diffZipPath)
    return (True, prefix + diffZipName)


        