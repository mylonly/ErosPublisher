from django.shortcuts import render
from rest_framework import generics, views
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from django.contrib import auth
from . import serializers
# Create your views here.


class login(views.APIView):

  def post(self, request, *args, **kwargs):
    
    username = request.data.get("username")
    password = request.data.get("password")

    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return ErosResponse()
    else:
      return ErosResponse(ErosResponseStatus.INVALID_USER)


class logout(views.APIView):
  def post(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      auth.logout(request)
      return ErosResponse()
    else:
      return ErosResponse(data=None, status=ErosResponseStatus.UNAUTHORIZED)

class profile(generics.GenericAPIView):
  serializer_class = serializers.UserSerializer
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      serializer = self.get_serializer(request.user)
      return ErosResponse(data=serializer.data, status=ErosResponseStatus.OK)
    else:
      return ErosResponse(data=None, status=ErosResponseStatus.UNAUTHORIZED)
    
