from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<search_term>[^\s\\/]+)/$', views.search, name='search')
]