from django.conf.urls import url
from . import views
app_name = "login"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^users/(?P<id>\d+)$', views.user, name='user'),
    url(r'^login$', views.login, name='login'),
    url(r'^success$', views.success, name='success'),
    url(r'^logout$', views.logout, name='logout')
]
