"""Import categories command.

This command imports categories from a csv file.

"""

import csv

from channels.models import Category, Channel
from django.core.management import BaseCommand
from django.db import transaction
from django.utils.text import slugify


class Command(BaseCommand):
    """Base class for the importcategories command.

    Parse and import a CSV with categories.
    """

    def add_arguments(self, parser):
        """Define command options along with the parser."""
        parser.add_argument(
            'channel_name',
            help='Name of the channel. e.g: Amazon.'
        )
        parser.add_argument(
            'csv_file',
            type=lambda file: csv.DictReader(open(file)),
            help='Filename of the CSV with the categories.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Create the channel entry and its categories."""
        channel_name = options.get('channel_name')
        csv_file = options.get('csv_file')

        # noinspection PyUnresolvedReferences
        channel, created = Channel.objects.get_or_create(
            reference=slugify(channel_name),
            defaults={'name': channel_name}
        )

        for line in csv_file:
            parent_node = None

            for name in map(str.strip, line.get('Category', '').split('/')):
                # noinspection PyUnresolvedReferences
                parent_node, created = Category.objects.get_or_create(
                    channel=channel,
                    parent=parent_node,
                    name=name
                )
