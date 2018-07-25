# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import QueryDict, HttpResponse, JsonResponse
from django.views.generic import View, TemplateView, DeleteView, ListView
from inception import table_structure

class inception_commit(TemplateView):
    template_name = 'inception/inception_commit.html'

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        print webdata
        table_structure(webdata['sqlcontent'])
        return JsonResponse({'status': 0})

