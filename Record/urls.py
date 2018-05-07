#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-02 16:01:05
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: description


from django.urls import path
from Record.views import CheckRecord,RecordList

urlpatterns = [
  path('check',CheckRecord.as_view()),
  path('list',RecordList.as_view())
]