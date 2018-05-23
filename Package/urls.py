#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-24 15:43:05
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: Package路由


from django.urls import path
from Package.views import PackageList,PackageCreate,PackageDelete,PackageUpdate,PackageUpload,PackageVersion

urlpatterns = [
  path('list',PackageList.as_view()),
  path('create',PackageCreate.as_view()),
  path('delete',PackageDelete.as_view()),
  path('update',PackageUpdate.as_view()),
  path('upload',PackageUpload.as_view()),
  path('version',PackageVersion.as_view())
]
