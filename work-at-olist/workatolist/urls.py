"""URLs for the project."""

from django.conf.urls import include, url
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^api/v1/', include('channels.urls', namespace='channels')),
    url(r'^.*$', RedirectView.as_view(url='/api/v1/', permanent=False)),
]
