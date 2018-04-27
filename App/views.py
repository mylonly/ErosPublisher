from django.shortcuts import render
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from rest_framework import views,generics
from App.models import App
from App.serializers import AppSerializer

# Create your views here.
class AppList(generics.ListAPIView):
  queryset = App.objects.all()
  serializer_class = AppSerializer

  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return ErosResponse(data=serializer.data)


class CreateApp(generics.CreateAPIView):
  serializer_class = AppSerializer
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return ErosResponse(data=serializer.data)
    return ErosResponse(status=ErosResponseStatus.SERIALIZED_FAILED)


  