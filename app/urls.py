from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^healthcheck/?$', views.healthcheck, name='healthcheck'),
    url(r'^result/?$', views.result, name='result'),
]
