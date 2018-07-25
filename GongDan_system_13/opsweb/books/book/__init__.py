# coding=utf8
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from books.models import Publish, Author, Book
from books.forms import PublishForm, BookForm, AuthorForm

import json
import logging

logger = logging.getLogger('opsweb')


class BookListView(LoginRequiredMixin, PaginationMixin, ListView):
    '''
    动作：getlist, create
    '''
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "book_list"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(BookListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                       Q(authors__name__icontains=self.keyword) |
                                       Q(publisher__name__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加书成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)


class BookDetailView(LoginRequiredMixin, DetailView):
    '''
    动作：getone, update, delete
    '''
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = 'book'
    next_url = '/books/booklist/'

    def get_context_data(self, **kwargs):
        self.keyword = self.request.GET.get('keyword', '').strip()
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = BookForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {"code": 0, "result": "更新书成功", 'next_url': self.next_url}
        else:
            res = {"code": 1, "errmsg": form.errors, 'next_url': self.next_url}
        return render(request, settings.JUMP_PAGE, res)
        # return HttpResponseRedirect(reverse('books:publish_detail',args=[pk]))

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 通过出版社对象查所在该出版社的书籍，如果有关联书籍不可以删除，没有关联书籍可以删除
        try:
            obj = self.model.objects.get(pk=pk)
            if not obj.book_set.all():
                self.model.objects.filter(pk=pk).delete()
                res = {"code": 0, "result": "删除书成功"}
            else:
                res = {"code": 1, "errmsg": "该书籍,请联系管理员"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)

