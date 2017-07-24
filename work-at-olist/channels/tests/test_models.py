"""Test models Channel and Category."""

from channels.models import Category, Channel
from django.test import TestCase


class ChannelTest(TestCase):
    """Test cases for Channel model."""

    channel_name = 'Name of the channel'
    channel_reference = 'name-of-the-channel'

    def setUp(self):
        """Create Channel object."""
        Channel.objects.create(name=self.channel_name)

    def test_channel_name(self):
        """Test if Channel was created."""
        self.assertTrue(Channel.objects.get(name=self.channel_name))

    def test_channel_reference(self):
        """Test if Channel reference is correct."""
        self.assertTrue(Channel.objects.get(reference=self.channel_reference))


class CategoryTest(TestCase):
    """Test cases for the Category model."""

    channel_name = 'Amazon'
    categories = {
        'parent': {'name': 'Books', 'reference': 'amazon-books'},
        'child': {'name': 'Fantasy', 'reference': 'amazon-books-fantasy'}
    }

    def setUp(self):
        """Create categories for the test cases."""
        self.channel = Channel.objects.create(name=self.channel_name)
        self.parent_category = Category.objects.create(
            channel=self.channel,
            name=self.categories.get('parent').get('name'),
            parent=None
        )
        self.child_category = Category.objects.create(
            channel=self.channel,
            name=self.categories.get('child').get('name'),
            parent=self.parent_category
        )

    def test_parent_category_reference(self):
        """Test if parent category name and reference is correct."""
        self.assertEqual(
            self.child_category.parent.name,
            self.categories.get('parent').get('name')
        )

        self.assertEqual(
            self.child_category.parent.reference,
            self.categories.get('parent').get('reference')
        )

    def test_child_category_reference(self):
        """Test if child category name and reference is correct."""
        self.assertEqual(
            self.child_category.reference,
            self.categories.get('child').get('reference')
        )

        self.assertEqual(
            self.child_category.name,
            self.categories.get('child').get('name')
        )

    def test_categories_created(self):
        """Check if all categories were created."""
        self.assertEqual(
            Category.objects.filter(
                channel__name=self.channel_name,
            ).count(),
            2
        )
