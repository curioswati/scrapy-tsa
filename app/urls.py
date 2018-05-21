from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin$', include(admin.site.urls)),
    url(r'^healthcheck/?$', views.healthcheck, name='healthcheck'),
    url(r'^result/?$', views.result, name='result'),
]
