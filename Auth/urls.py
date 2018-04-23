#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-23 15:32:59
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: Auth url 路由

from django.urls import path
from Auth.views import login,logout,profile

urlpatterns = [
  path('login',login.as_view()),
  path('logout',logout.as_view()),
  path('profile',profile.as_view())
]
