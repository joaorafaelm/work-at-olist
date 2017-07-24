"""Test API endpoints for Category and Channel."""

import json

from channels.models import Category, Channel
from django.test import Client, TestCase


class BaseViewTest(TestCase):
    """Base Test case for creation of Channel and Category."""

    channel_info = {'name': 'Amazon', 'reference': 'amazon'}
    categories = {
        'parent': {'name': 'Books', 'reference': 'amazon-books'},
        'child': {'name': 'Fantasy', 'reference': 'amazon-books-fantasy'}
    }
    api_base_url = '/api/v1'
    client = Client()

    def setUp(self):
        """Create channel and categories for the test cases."""
        self.channel = Channel.objects.create(
            name=self.channel_info.get('name')
        )
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


class ChannelViewTest(BaseViewTest):
    """Test cases for list and detail of the channel api."""

    endpoint = 'channel'

    def test_channel_list(self):
        """Test if the endpoint lists the correct number of channel(s)."""
        response = self.client.get(
            '{base}/{endpoint}/'.format(
                base=self.api_base_url,
                endpoint=self.endpoint
            )
        )
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(content.get('count'), 1)

    def test_channel_detail(self):
        """Test if the endpoint correctly shows the channel details."""
        response = self.client.get(
            '{base}/{endpoint}/{identifier}/'.format(
                base=self.api_base_url,
                endpoint=self.endpoint,
                identifier=self.channel_info.get('reference')
            )
        )
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(content.get('name'), self.channel_info.get('name'))
        self.assertEqual(
            content.get('reference'), self.channel_info.get('reference')
        )
        self.assertEqual(len(content.get('categories')), 2)


class CategoryViewTest(BaseViewTest):
    """Test cases for list and detail of the category api."""

    endpoint = 'category'

    def test_category_list(self):
        """Test if the endpoint lists the correct number of categories."""
        response = self.client.get(
            '{base}/{endpoint}/'.format(
                base=self.api_base_url,
                endpoint=self.endpoint
            )
        )
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(content.get('count'), 2)

    def test_parent_category_detail(self):
        """Test if the endpoint correctly shows the parent category details."""
        response = self.client.get(
            '{base}/{endpoint}/{identifier}/'.format(
                base=self.api_base_url,
                endpoint=self.endpoint,
                identifier=self.categories.get('parent').get('reference')
            )
        )
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(
            content.get('name'), self.categories.get('parent').get('name')
        )
        self.assertEqual(
            content.get('reference'),
            self.categories.get('parent').get('reference')
        )
        self.assertEqual(content.get('parent'), None)
        self.assertEqual(len(content.get('children')), 1)

    def test_child_category_detail(self):
        """Test if the endpoint correctly shows the child category details."""
        response = self.client.get(
            '{base}/{endpoint}/{identifier}/'.format(
                base=self.api_base_url,
                endpoint=self.endpoint,
                identifier=self.categories.get('child').get('reference')
            )
        )
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(
            content.get('name'), self.categories.get('child').get('name')
        )
        self.assertEqual(
            content.get('reference'),
            self.categories.get('child').get('reference')
        )
        self.assertEqual(
            content.get('parent').get('reference'),
            self.categories.get('parent').get('reference')
        )
        self.assertEqual(len(content.get('children')), 0)
