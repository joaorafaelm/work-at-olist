"""Channels API serializers."""

from channels.models import Category, Channel
from rest_framework.serializers import CharField, ModelSerializer
from rest_framework_recursive.fields import RecursiveField


class ParentSerializer(ModelSerializer):
    """Serializer for the parent category."""

    parent = RecursiveField(allow_null=True)

    class Meta:
        """Serializes the fields: name, reference and parent."""

        model = Category
        fields = ('name', 'reference', 'parent')


class ChildrenSerializer(ModelSerializer):
    """Recursively serializes the children of a category."""

    children = RecursiveField(allow_null=True, many=True)

    class Meta:
        """Serializes the fields: name, reference and children."""

        model = Category
        fields = ('name', 'reference', 'children')


class CategoryListSerializer(ModelSerializer):
    """Serializer for a list of categories of a channel."""

    channel = CharField(source='channel.reference')
    parent_reference = CharField(source='parent.reference')

    class Meta:
        """Serializes the fields: reference, name and the parent reference."""

        model = Category
        fields = ('reference', 'name', 'channel', 'parent_reference')


class CategoryDetailSerializer(ModelSerializer):
    """Serializer for the details of a category."""

    parent = ParentSerializer()
    children = ChildrenSerializer(many=True)
    channel = CharField(source='channel.reference')

    class Meta:
        """Serializes the fields: reference, name, parent and children."""

        model = Category
        fields = ('reference', 'name', 'channel', 'parent', 'children')


class ChannelListSerializer(ModelSerializer):
    """Serializer for a list of channels."""

    class Meta:
        """Serializes the fields: name and reference."""

        model = Channel
        fields = ('name', 'reference')


class ChannelDetailSerializer(ModelSerializer):
    """Serializer for the details of a channel."""

    categories = CategoryListSerializer(many=True)

    class Meta:
        """Serializes the fields: name, reference and categories."""

        model = Channel
        fields = ('name', 'reference', 'categories')
