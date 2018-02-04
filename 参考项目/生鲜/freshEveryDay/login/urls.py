from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^login/$',login,name='login'),    
    url(r'^loginHandler/$',loginHandler,name='loginHandler'),
    url(r'^registe/$',registe,name='registe'),
    url(r'^registHandler/$',registHandler,name='registHandler'),
    url(r'^saveDataHandler/$',saveDataHandler,name='saveDataHandler'),
    ] 