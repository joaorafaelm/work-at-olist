"""URLs for the project."""

from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/v1/', include('channels.urls', namespace='channels')),
]
