from django.shortcuts import render
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from rest_framework import views,generics
from Package.models import Package
from Package.serializers import PackageSerializer
# Create your views here.


class PackageList(generics.GenericAPIView):
  queryset = Package.objects.all()
  serializer_class = PackageSerializer

  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return ErosResponse(data=serializer.data)


class PackageCreate(generics.CreateAPIView):
  serializer_class = PackageSerializer
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return ErosResponse(data=serializer.data)
    return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED)

  


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