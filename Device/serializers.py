#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 21:54:25
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: 设备序列化类


from rest_framework import serializers
from Device.models import Device
class DeviceSerializers(serializers.ModelSerializer):
  class Meta:
    model = Device
    fields = '__all__'