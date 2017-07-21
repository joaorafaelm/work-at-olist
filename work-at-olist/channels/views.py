"""Views for the Channel and Category API."""

from channels.models import Category, Channel
from channels.serializers import (
    CategoryDetailSerializer, CategoryListSerializer,
    ChannelDetailSerializer, ChannelListSerializer
)
from rest_framework.viewsets import ReadOnlyModelViewSet


class MultiSerializerViewSet(ReadOnlyModelViewSet):
    """Provides multiple serializer declaration in a single view."""

    serializers = {'default': None}

    def get_serializer_class(self):
        """Select the serializer based on the action."""
        return self.serializers.get(
            self.action, self.serializers.get('default')
        )


class ChannelViewSet(MultiSerializerViewSet):
    """List all channels and details if one is specified."""

    # noinspection PyUnresolvedReferences
    queryset = Channel.objects.all()
    lookup_field = 'reference'
    serializers = {
        'list': ChannelListSerializer,
        'retrieve': ChannelDetailSerializer
    }


class CategoryViewSet(MultiSerializerViewSet):
    """List all categories or details of one if reference is specified."""

    queryset = Category.objects.all()
    lookup_field = 'reference'
    serializers = {
        'list': CategoryListSerializer,
        'retrieve': CategoryDetailSerializer
    }
