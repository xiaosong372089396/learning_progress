# -*- coding:UTF-8 -*-


from django.conf.urls import url
from views import *
import views
# from cmdb.views import product, views
import product

urlpatterns = [
    url('^product_detail/(?P<pk>[0-9]+)?/$', product.ProductDetailView.as_view(), name='product_detail'),
    url('^product_add/$', product.ProductAddView.as_view(), name='product_add'),
    url('^import_data/$', views.ImportDataView.as_view(), name='import_data'),
#    url('^hosts/$', views.HostListView.as_view(), name='host_list'),
   url('^host/(?P<pk>[0-9]+)?/$', views.HostEditView.as_view(), name='host_edit'),

]