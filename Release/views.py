from django.shortcuts import render
from rest_framework import views,generics
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from App.models import App
from Device.models import Device
from Package.models import Package
from Release.models import Record, Release
from Release.serializers import RecrodSerializer, ReleaseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.serializers import ValidationError
import bsdiff4
from ErosUpdate.settings import MEDIA_ROOT
import os.path
import logging
# Create your views here.


class RecordUpdate(generics.GenericAPIView):

  serializer_class = RecrodSerializer

  def post(self, request, *args, **kwargs):
   
      appName = request.data.get('appName')
      deviceToken = request.data.get('deviceToken')
      appPlatform = request.data.get('appPlatform')
      appVersion = request.data.get('appVersion')
      jsMD5 = request.data.get('jsMD5')
      isDiff = request.data.get('isDiff')
      if appName is None or deviceToken is None or appPlatform is None or appVersion is None:
        return ErosResponse(status=ErosResponseStatus.PARAMS_ERROR)
      try:
        record = None
        package = None
        records = Record.objects.filter(appName=appName, deviceToken=deviceToken)
        if len(records) > 0:
          record = records[0]
          updateJSVersion = record.updateJSVersion
          serializer= self.get_serializer(record, data=request.data)
          if serializer.is_valid():
            record = serializer.save()
            oldPackages = Package.objects.filter(appName=appName,jsMD5=jsMD5)
            if len(oldPackages) > 0:
              record.jsVersion = oldPackages[0].jsVersion
            record.save()
          else:
            raise ValidationError("Params Error, Serializer Failed!!!")
          package = self.lastPackage(appName, appPlatform, appVersion, updateJSVersion)
        else:
          serializer = self.get_serializer(data=request.data)
          if serializer.is_valid():
            record = serializer.save()
            oldPackages = Package.objects.filter(appName=appName,jsMD5=jsMD5)
            if len(oldPackages) > 0:
              record.jsVersion = oldPackages[0].jsVersion
            package = self.lastPackage(appName, appPlatform, appVersion)
            record.updateJSVersion = package.jsVersion
            record.save()
          else:
            raise ValidationError("Params Error, Serializer Failed!!!")

        if jsMD5 != package.jsMD5 and isDiff: #生成增量包
          (isDiff,jsPath) = self.diffPakagePath(jsMD5,package.jsMD5)
          resData = {
            "diff":isDiff,
            "path":jsPath,
            "showUpdateAlert":package.showUpdateAlert,
            "changelog":package.changelog,
          }
          return ErosResponse(data=resData)
        elif not isDiff:
          resData = {
            "diff":False,
            "path":package.jsPath,
            "showUpdateAlert":package.showUpdateAlert,
            "changelog":package.changelog,
          }
          return ErosResponse(data=resData)
        else:
          return ErosResponse(status=ErosResponseStatus.IS_LASTEST_PACKAGE)
      except Package.DoesNotExist as e:
        return ErosResponse(status=ErosResponseStatus.NOT_FOUND,detail=str(e))
      except NameError as e:
        return ErosResponse(status=ErosResponseStatus.NOT_FOUND, detail=str(e))
      except ValidationError as e:
        return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED,detail=str(e))

  def lastPackage(self, appName, appPlatform, appVersion, jsVersion=None):
    package = None
    packages = None
    if appPlatform == 'iOS':
      packages = Package.objects.filter(appName=appName, published=True, ios=appVersion)
    elif appPlatform == 'Android':
      packages = Package.objects.filter(appName=appName, published=True, android=appVersion)
    else:
      raise NameError("UnSupport Platform[%s]" % (appPlatform))

    packages = packages.order_by('-timestamp')

    if(jsVersion):
      packages = packages.filter(jsVersion=jsVersion)
    
    if len(packages) > 0:
      package = packages[0]
    else:
      raise Package.DoesNotExist("Package Does Not Found")
    
    return package

  def diffPackage(oldMD5,newMD5):
    
    diffZip = MEDIA_ROOT+oldMD5+'+'+newMD5+'.zip'

    oldZip = MEDIA_ROOT + oldMD5 + '.zip'
    newZip = MEDIA_ROOT + newMD5 + '.zip'

    #先判断diff文件存不存在,存在说明之前生成过这个增量包，直接返回
    exsit = os.path.isfile(diffZip) 
    if exsit:
      return (True,diffZip)

    #判断老的js包存不存在，不存在返回最新全量包的地址
    exsit = os.path.isfile(oldZip) 
    if not exsit:
      return (False,newZip)

    exsit = os.path.isfile(newZip)
    if not exsit:
      return (False,None)

    oldZipFile = open(oldZip, 'rb')
    oldZipBytes = oldZipFile.read()
    oldZipFile.close()

    newZipFile = open(newZip, 'rb')
    newZipBytes = newZipFile.read()
    newZipFile.close()

    diffZipBytes = bsdiff4(oldZipBytes, newZipBytes)
    diffZipFile = open(diffZip, 'wb')
    diffZipFile.write(diffZipBytes)
    diffZipFile.close
    return (True, diffZip)


class RecordList(generics.GenericAPIView):
  queryset = Record.objects.all()
  serializer_class = RecrodSerializer
  filter_backends = (DjangoFilterBackend,OrderingFilter)
  filter_fields = '__all__'
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




class AddRelease(generics.CreateAPIView):
  serializer_class = ReleaseSerializer
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return ErosResponse(data=serializer.data)
    return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED,detail=serializer.errors)


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

    jsVersion = Release.gotHit(data) #获取命中的更新包
    if not jsVersion:
      return ErosResponse(status=ErosResponseStatus.IS_LASTEST_PACKAGE)
    data['updateJSVersion'] = jsVersion
    
    self.updateRecord(data)  #更新记录

    try:
      package = Package.objects.get(jsVersion=jsVersion)
      newMD5 = package.jsMD5
      oldMD5 = data['jsMD5']
      isDiff = data['isDiff']
      jsPath = package.jsPath
      if newMD5 == oldMD5:
        return ErosResponse(status=ErosResponseStatus.IS_LASTEST_PACKAGE)
      if isDiff:
        (isDiff, jsPath) = self.diffPackage(oldMD5,newMD5)
      
      resData = {
          "diff":isDiff,
          "path":jsPath,
          "showUpdateAlert":package.showUpdateAlert,
          "changelog":package.changelog,
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
  
  def diffPackage(self, oldMD5, newMD5):
    
    diffZip = MEDIA_ROOT+oldMD5+'+'+newMD5+'.zip'

    oldZip = MEDIA_ROOT + oldMD5 + '.zip'
    newZip = MEDIA_ROOT + newMD5 + '.zip'

    #先判断diff文件存不存在,存在说明之前生成过这个增量包，直接返回
    exsit = os.path.isfile(diffZip) 
    if exsit:
      return (True,diffZip)

    #判断老的js包存不存在，不存在返回最新全量包的地址
    exsit = os.path.isfile(oldZip) 
    if not exsit:
      return (False,newZip)

    exsit = os.path.isfile(newZip)
    if not exsit:
      return (False,None)

    oldZipFile = open(oldZip, 'rb')
    oldZipBytes = oldZipFile.read()
    oldZipFile.close()

    newZipFile = open(newZip, 'rb')
    newZipBytes = newZipFile.read()
    newZipFile.close()

    diffZipBytes = bsdiff4(oldZipBytes, newZipBytes)
    diffZipFile = open(diffZip, 'wb')
    diffZipFile.write(diffZipBytes)
    diffZipFile.close
    return (True, diffZip)

    
    


        