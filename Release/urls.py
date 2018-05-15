#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-02 16:01:05
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: description


from django.urls import path
from Release.views import CheckUpdate,RecordList,AddRelease,ReleaseList

urlpatterns = [
  path('check',CheckUpdate.as_view()),
  path('list',ReleaseList.as_view()),
  path('add', AddRelease.as_view()),
  path('records', RecordList.as_view())
]