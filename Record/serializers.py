#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-02 15:09:59
# @Author  : root (root@mylonly.com)
# @Version : 1.0.0
# @Description: description




from rest_framework import serializers
from Record.models import Record

class RecrodSerializer(serializers.ModelSerializer):
  class Meta:
    model = Record
    fields = '__all__'

  def validate(self, data):
    ios = data.get('iOS')
    android = data.get('android')
    if ios and android:
      raise serializers.ValidationError("Param [iOS] and [android] can only exsit one")
    if ios is None and android is None:
      raise serializers.ValidationError("Param [iOS] and [android] must have one")
    return data
