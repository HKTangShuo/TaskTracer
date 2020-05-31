#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings
import datetime


class Tracer(object):

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """ 如果用户已登录，则request中赋值 """
        request.tracer = Tracer()
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.tracer.user:
            return redirect('login')
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()

        # 判断是否已过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            # status 2 已支付   price_policy__category 1 免费版
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()

        request.tracer.price_policy = _object.price_policy

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # url 是否以manage开头
        if not request.path_info.startswith('/manage/'):
            return

        # project_id 是否是我的或者我参与的
        project_id = callback_kwargs['project_id']
        # 是否是我创建的
        project_obj = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_obj:
            request.tracer.project = project_obj
            return
        # 是否是我参与的
        project_user_obj = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_obj:
            request.tracer.project = project_user_obj.project
            return

        return redirect('project_list')
