#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 21:45:18
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: App 序列化类

import os
from rest_framework.serializers import ModelSerializer
from App.models import App

class AppSerializer(ModelSerializer):
  class Meta:
    model = App
    fields = '__all__'