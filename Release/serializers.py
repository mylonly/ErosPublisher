#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-02 15:09:59
# @Author  : root (root@mylonly.com)
# @Version : 1.0.0
# @Description: description




from rest_framework import serializers
from Release.models import Record, Release

class RecrodSerializer(serializers.ModelSerializer):
  class Meta:
    model = Record
    exclude = ('ip','area')

  
  

class ReleaseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Release
    fields = '__all__'