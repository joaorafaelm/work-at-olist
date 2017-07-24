"""Test file for the importcategories command."""

from os.path import join

from channels.models import Category, Channel
from django.core.management import call_command, CommandError
from django.test import TestCase
from workatolist.settings import BASE_DIR


class TestImportCategoriesCommand(TestCase):
    """Tests for the "importcategories" command."""

    channel = 'Amazon'
    csv_file = join(BASE_DIR, 'channels/tests/sample.csv')

    def setUp(self):
        """Call importcategories command before test cases."""
        call_command('importcategories', self.channel, self.csv_file)

    def test_channel_created(self):
        """Check if the channel was created."""
        self.assertTrue(Channel.objects.get(name=self.channel))

    def test_categories_created(self):
        """Test if all the categories from the sample csv were created."""
        self.assertEqual(
            Category.objects.filter(channel__name=self.channel).count(),
            29
        )

    def test_root_node_categories(self):
        """Test if all the top categories were created."""
        self.assertEqual(
            Category.objects.filter(
                channel__name=self.channel,
                parent=None
            ).count(),
            4
        )

    def test_invalid_arguments(self):
        """Check if the command fails using invalid arguments."""
        self.assertRaises(
            CommandError, call_command, 'importcategories'
        )
        self.assertRaises(
            CommandError, call_command, 'importcategories', 'Amazon'
        )

    def test_reimport(self):
        """Test if importing the file again works correctly."""
        call_command('importcategories', self.channel, self.csv_file)
        self.assertTrue(Channel.objects.get(name=self.channel))
        self.assertEqual(
            Category.objects.filter(channel__name=self.channel).count(),
            29
        )
