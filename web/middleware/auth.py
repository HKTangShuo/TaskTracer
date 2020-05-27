#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """ 如果用户已登录，则request中赋值 """

        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.tracer:
            return redirect('login')
