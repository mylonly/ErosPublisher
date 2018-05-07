from django.shortcuts import render
from rest_framework import views,generics
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from App.models import App
from Device.models import Device
from Package.models import Package
from Record.models import Record
from Record.serializers import RecrodSerializer
# Create your views here.


class CheckRecord(generics.GenericAPIView):

  serializer_class = RecrodSerializer

  def get(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.query_params)
    if serializer.is_valid():
      appName = request.query_params['appName']
      deviceToken = request.query_params['deviceToken']
      ios = request.query_params.get('iOS')
      android = request.query_params.get('android')
      try:
        record = Record.objects.get(appName=appName, deviceToken=deviceToken)
        updateJSVersion = record.updateJSVersion
        package = None
        if updateJSVersion:
          if ios:
            package = Package.objects.get(appName=appName, jsVersion=updateJSVersion, published=True, ios=ios)
          if android:
            package = Package.objects.get(appName=appName, jsVersion=updateJSVersion, published=True, android=android)
        else:
          package = self.lastPackage(appName)
        
        resData = {
          "diff":False,
          "path":package.jsPath
        }
        return ErosResponse(data=resData)

      except Record.DoesNotExist as e:
        
        # record = serializer.save()
        package = self.lastPackage(appName)
        if package is None:
          return ErosResponse(status=ErosResponseStatus.NOT_FOUND, detail="App[%s] does not exsit one published package" % (appName))
        record = serializer.save()
        record.updateJSVersion = package.jsVersion
        record.save()
        response = {
          "diff":False,
          "path":package.jsPath
        }
        return ErosResponse(data=response)
      except Package.DoesNotExist as e:
        return ErosResponse(status=ErosResponseStatus.NOT_FOUND,detail=str(e))
    else:
      return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED,detail=serializer.errors)

  def lastPackage(self, appName):
    packages = Package.objects.filter(appName=appName, published=True).order_by('timestamp').aesc()
    if len(packages) > 0:
      return packages[0]
    else:
      return None


class RecordList(generics.GenericAPIView):
  queryset = Record.objects.all()
  serializer_class = RecrodSerializer

  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return ErosResponse(data=serializer.data)