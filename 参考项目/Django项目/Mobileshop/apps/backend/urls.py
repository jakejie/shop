from django.conf.urls import url, include
from .views import ProductList

urlpatterns = [
    url(r'^user/', include('user.urls')),
    url(r'^$', ProductList.as_view()),
]