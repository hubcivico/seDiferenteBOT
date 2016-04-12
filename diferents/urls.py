from django.conf.urls import include, url
from diferents.views import *

urlpatterns = [
    url(r'^$', get_update)
]