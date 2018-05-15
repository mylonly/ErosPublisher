#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-24 11:39:23
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: Package模块序列化


from rest_framework import serializers
from Package.models import Package

class PackageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Package
    fields = '__all__'