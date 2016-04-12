from django.conf.urls import include, url
from diferentes.views import *

urlpatterns = [
    url(r'^$', get_update)
]
