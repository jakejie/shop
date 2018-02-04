from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.order),
    # url(r'^goods$', views.home_list_page),
]
