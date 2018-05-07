#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 21:45:18
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: App 序列化类

import os
from rest_framework import serializers
from App.models import App

class AppSerializer(serializers.ModelSerializer):
  class Meta:
    model = App
    fields = '__all__'

class UpdateResultSerializer(serializers.Serializer):
  diff = serializers.BooleanField()
  path = serializers.URLField()
