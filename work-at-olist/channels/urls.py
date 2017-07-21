"""URL definition for the project API."""

from channels.views import CategoryViewSet, ChannelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'channel', ChannelViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = router.urls
