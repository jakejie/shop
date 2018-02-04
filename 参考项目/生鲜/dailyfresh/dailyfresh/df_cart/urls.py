from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'index', views.index),
    url(r'addcart/(\d+)_(\d+)', views.addcart),
    url(r'tocart/(\d+)_(\d+)', views.tocart),
    url(r'delete/(\d+)', views.delete),
]