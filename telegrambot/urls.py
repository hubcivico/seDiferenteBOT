from django.contrib import admin
from django.conf.urls import include, url, patterns
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^diferentes/', include('diferentes.urls')),
    url(r'^diferents/', include('diferents.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
]
