#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-23 15:21:37
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: 通用返回格式

import os
from django.http import JsonResponse
from enum import Enum,unique

class ErosResponseStatus(Enum):
  OK = ("Operation Success", 0)
  INVALID_USER = ("Login Failed", 1)
  UNAUTHORIZED = ("unauthorized", 2)
  SERIALIZED_FAILED = ("Serialized Failed", 3)
  PARAMS_ERROR = ("Params Error", 4)
  NOT_FOUND = ("Not Found", 5)

class ErosResponse(JsonResponse):

  def __init__(self, data=None, status=ErosResponseStatus.OK):
    tips = status.value[0]
    code = status.value[1]

    response = {
      'status':code,
      'message':tips,
      'data':data
    }
    super(ErosResponse, self).__init__(response, status=200)

    ###允许跨域
    # self["Access-Control-Allow-Origin"] = "*"
    # self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # self["Access-Control-Max-Age"] = "1000"
    # self["Access-Control-Allow-Headers"] = "Authorization,Origin, X-Requested-With, Content-Type, Accept"
