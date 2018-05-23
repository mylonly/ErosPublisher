from django.shortcuts import render
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from rest_framework import views,generics
from Package.models import Package
from Package.serializers import PackageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FileUploadParser,MultiPartParser
import zipfile
from ErosUpdate.settings import MEDIA_ROOT,MEDIA_URL
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from rest_framework.permissions import AllowAny

# Create your views here.


class PackageList(generics.ListAPIView):
  queryset = Package.objects.all()
  serializer_class = PackageSerializer
  filter_backends = (DjangoFilterBackend,OrderingFilter)
  filter_fields = ('appName','published') 
  ordering_fields = ('id', 'timestamp')

  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return ErosResponse(data=response.data)

    serializer = self.get_serializer(queryset, many=True)
    return ErosResponse(data=serializer.data)


class PackageCreate(generics.CreateAPIView):
  serializer_class = PackageSerializer
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return ErosResponse(data=serializer.data)
    return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED, detail=serializer.errors)

  
class PackageUpdate(generics.GenericAPIView):
  serializer_class = PackageSerializer
  def post(self, request, *args, **kwargs):
    ID = request.data["id"]
    if ID is None:
      return ErosResponse(status=ErosResponseStatus.PARAMS_ERROR, detail="param [id] is missing...")
    try:
      instance = Package.objects.get(id=ID)
      partial = kwargs.pop('partial', False)
      serializer = self.get_serializer(instance, data=request.data, partial=partial)
      if serializer.is_valid():
         serializer.save()
         return ErosResponse(data=serializer.data)
      else:
        return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED)
      if getattr(instance, '_prefetched_objects_cache', None):
          # If 'prefetch_related' has been applied to a queryset, we need to
          # forcibly invalidate the prefetch cache on the instance.
          instance._prefetched_objects_cache = {}
    except Package.DoesNotExist:
      return ErosResponse(status=ErosResponseStatus.NOT_FOUND, detail="Package not found")

class PackageDelete(generics.GenericAPIView):
  def post(self, request, *args, **kwargs):
    package_id = request.data.get("package_id")
    if package_id == None:
      return ErosResponse(data=None, status=ErosResponseStatus.PARAMS_ERROR)
    else:
      try:
        package = Package.objects.get(id=package_id)
        package.delete()
        return ErosResponse()
      except Package.DoesNotExist:
        return ErosResponse(status=ErosResponseStatus.NOT_FOUND)

class PackageUpload(views.APIView):
  parser_classes = (MultiPartParser,)
  def post(self, request, *args, **kwargs):

    try:
      file = request.FILES['file']
      default_storage.save(file.name, ContentFile(file.read()))
      zfile = zipfile.ZipFile(MEDIA_ROOT+file.name)
      
      

      md5File = zfile.open('md5.json')
      jsonObj = json.load(md5File)

      responseData = {
        "appName": jsonObj['appName'],
        "jsMD5": jsonObj['jsVersion'],
        "android": jsonObj['android'],
        "ios": jsonObj['iOS'],
        "timestamp": jsonObj['timestamp'],
        "jsPath": 'http://'+request.get_host()+MEDIA_URL+file.name
      }
      zfile.close()
      return ErosResponse(data=responseData)
    except Exception as e:
      return ErosResponse(status=ErosResponseStatus.UPLOAD_FAILED,detail=str(e))

class PackageVersion(generics.GenericAPIView):
  serializer_class = PackageSerializer
  permission_classes = (AllowAny,)

  def get(self, request, *args, **kwargs):
    jsMD5 = request.query_params.get('jsMD5')
    if not jsMD5:
      return ErosResponse(status=ErosResponseStatus.PARAMS_ERROR, detail='missing jsMD5')
    
    try:
      queryset = Package.objects.get(jsMD5=jsMD5)
      serializer = self.get_serializer(queryset)
      return ErosResponse(data=serializer.data)
    except Package.DoesNotExist:
      return ErosResponse(status=ErosResponseStatus.NOT_FOUND, detail='Package [%s] Not Found' % (jsMD5))
