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
  OK = ("操作成功", 0)
  INVALID_USER = ("不合法用户", 1)
  UNAUTHORIZED = ("未认证", 2)
  SERIALIZED_FAILED = ("序列化失败", 3)
  PARAMS_ERROR = ("参数错误", 4)
  NOT_FOUND = ("不存在", 5)
  EXECEPTION = ("捕获到异常", 6)
  UPLOAD_FAILED = ("上传失败", 7)
  IS_LASTEST_PACKAGE = ("已经是最新的包,不需要更新", 4000)
  PACKAGE_NOT_FOUND = ("更新包找不着", 4001)

class ErosResponse(JsonResponse):

  def __init__(self, data=None, status=ErosResponseStatus.OK, detail=None):
    tips = status.value[0]
    code = status.value[1]

    response = {
      'resCode':code,
      'msg':tips,
      'detail':detail,
      'data':data
    }
    super(ErosResponse, self).__init__(response, status=200)

    ###允许跨域
    # self["Access-Control-Allow-Origin"] = "*"
    # self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # self["Access-Control-Max-Age"] = "1000"
    # self["Access-Control-Allow-Headers"] = "Authorization,Origin, X-Requested-With, Content-Type, Accept"
