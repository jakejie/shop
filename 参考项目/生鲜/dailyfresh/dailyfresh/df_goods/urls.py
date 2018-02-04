from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home_list_page),
    # url(r'^goods$', views.home_list_page),
    url(r'^typeInfo', views.typeInfo),
    url(r'^detail', views.detail),
]
