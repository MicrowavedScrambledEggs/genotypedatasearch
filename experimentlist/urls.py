from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data_source/$', views.datasource, name='datasource'),
    # url(r'^(?P<search_term>[^\s\\/]+)/$', views.search, name='search')
]