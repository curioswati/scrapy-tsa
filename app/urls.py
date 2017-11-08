from django.conf.urls  import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^healthcheck/?$', views.healthcheck, name='healthcheck'),
    url(r'^get_mood/?$', views.get_mood, name='get_mood'),
]
