#! /usr/bin env python3
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http.request import QueryDict
from django.views import View
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest


# 渲染并进行数据处理
class BaseView(View):
    template_name = None

    def get(self, request, *args, **kwargs):

        # 数据处理
        if hasattr(self, 'prepare'):
            getattr(self, 'prepare')(request, *args, **kwargs)

        # 读取cookie
        if hasattr(self, 'handle_request_cookie'):
            getattr(self, 'handle_request_cookie')(request, *args, **kwargs)

        # 渲染
        response = render(request, self.template_name, self.get_context(request))

        # 设置cookie
        if hasattr(self, 'handle_response_cookie'):
            getattr(self, 'handle_response_cookie')(response, *args, **kwargs)

        return response

    """"
    def post(self, request, *args, **kwargs):
        # 数据处理
        if hasattr(self, 'prepare'):
            getattr(self, 'prepare')(request, *args, **kwargs)

        # 读取cookie
        if hasattr(self, 'handle_request_cookie'):
            getattr(self, 'handle_request_cookie')(request, *args, **kwargs)

        # 渲染
        response = render(request, self.template_name, self.get_context(request))

        # 设置cookie
        if hasattr(self, 'handle_response_cookie'):
            getattr(self, 'handle_response_cookie')(response, *args, **kwargs)
    """

    def get_context(self, request, *args, **kwargs):
        context = {}
        context.update(self.get_extra_context(request))
        return context

    def get_extra_context(self, request, *args, **kwargs):
        return {}


# 需要处理一些业务逻辑
class BaseRedirctView(View):
    redirct_url = None

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'handle'):
            getattr(self, 'handle')(request, *args, **kwargs)

        return HttpResponseRedirect(self.redirct_url)


# 处理Post请求，这里面不用渲染数据
# 一般来说，是不用渲染模板的，只需要返回json即可
class OperateView(View):
    form_cls = None

    def post(self, request, *args, **kwargs):
        # 数据清洗
        form = self.form_cls(request.POST.dict())
        if form.is_valid():
            handler = request.POST.get('type', '').lower()
            if hasattr(self, handler):
                return JsonResponse(getattr(self, handler)(request, **form.cleaned_data))
            else:
                return HttpResponseBadRequest('type 没有传递')
        else:
            return JsonResponse({'errorcode': -300, 'errormsg': form.errors})
