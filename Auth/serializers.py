#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-23 17:13:52
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: Auth Serializer

import os
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('password','user_permissions')