from django.shortcuts import render
from rest_framework import generics, views
from ErosUpdate.response import ErosResponse,ErosResponseStatus
from django.contrib import auth
from . import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import AllowAny
# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class login(views.APIView):
  authentication_classes = (BasicAuthentication,)
  permission_classes = (AllowAny,)
  def post(self, request, *args, **kwargs):
    
    username = request.data.get("username")
    password = request.data.get("password")

    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return ErosResponse()
    else:
      return ErosResponse(status=ErosResponseStatus.INVALID_USER)


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
    
