# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView,CreateView, UpdateView

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile


from .models import Tasks, ExecResult
from .Forms import TaskAddForm, TaskAdd1Form
import logging, traceback, json

logger = logging.getLogger("opsweb")


class TaskAddView(LoginRequiredMixin, View):
    def get(self, request):
        forms = TaskAddForm()
        return render(request, 'tasks/task_add.html', {'form': forms})

    def post(self, request):
        forms = TaskAddForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            '''
            name = forms.cleaned_data['name']
            playbook = forms.cleaned_data['playbook']
            auto_task = Tasks()
            auto_task.name = name
            auto_task.playbook = playbook
            auto_task.save()
            '''
            return HttpResponseRedirect(reverse('task:list'))
        else:
            return render(request, 'tasks/task_add.html', {'forms': forms, 'errmsg': '表单验证不通过!'})


class TaskListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
        任务列表
    """
    model = Tasks
    template_name = 'tasks/tasks_list.html'
    context_object_name = "tasklist"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword)|
                                       Q(detail_result__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context
