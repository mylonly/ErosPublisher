#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-23 17:13:52
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: Auth Serializer

import os
from rest_framework import serializers
from Auth.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    exclude = ('password','user_permissions')