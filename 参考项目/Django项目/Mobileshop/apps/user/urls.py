from django.conf.urls import url
from .views import UserShow, Register

urlpatterns = [
    url(r'^$', UserShow.as_view()),
    url(r'^register/', Register.as_view()),
]
