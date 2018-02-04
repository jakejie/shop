"""E_Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import goods.urls
import cart.urls
import User.urls
import order.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('goods.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^user/', include('User.urls')),
    url(r'^order/', include('order.urls'))
]

# 配置media的路由
from E_Shop import settings
if settings.DEBUG:
    from django.views.static import serve
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, kwargs={'document_root': settings.MEDIA_ROOT}))
