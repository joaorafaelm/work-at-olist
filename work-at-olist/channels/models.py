"""Models file.

All models of this module should be defined here.

"""

import uuid

from channels.utils import Attrgetter
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class BaseModel(models.Model):
    """Abstract model for Channel and Category classes.

    Models that inherit from this class get an auto filled slug property
    based on the models name property (Along with created/updated time).

    Correctly truncates the field to the max_length of the slug field.

    The following attributes can be overridden on a per model basis:
    * value_field_name - the field to slugify, it can be a tuple containing
                         multiple fields, default ('name',).
    * slug_field_name - the field to store the slugified value in,
                        default 'reference'.
    * slug_prefix - the field name which will be the prefix of the slug.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField(_('Time created'), auto_now_add=True)
    time_modified = models.DateTimeField(_('Time modified'), auto_now=True)
    reference = models.SlugField(_('Reference'), max_length=100, unique=True)

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs):
        """Auto creates an slugified reference based on another attribute."""
        value_field_name = getattr(self, 'value_field_name', ('name',))
        slug_field_name = getattr(self, 'slug_field_name', 'reference')
        slug_prefix = getattr(self, 'slug_prefix', None)

        # Retrieve the field where the slug will be stored
        slug_field = self._meta.get_field(slug_field_name)
        slug_len = slug_field.max_length

        # Get list of fields to create slug
        slug_list = Attrgetter(*value_field_name)(self)

        if isinstance(slug_list, tuple):
            slug_list = list(map(str, slug_list))
        else:
            slug_list = [slug_list]

        # Add prefix if it hasnt been added already
        if slug_prefix:
            slug_prefix_value = Attrgetter(slug_prefix)(self)
            if not slug_list[0].startswith(slug_prefix_value):
                slug_list.insert(0, slug_prefix_value + '-')

        slug_list = list(filter(None, slug_list))

        # Slugify the field
        slug = slugify('-'.join(slug_list))

        # Set the slug attribute value
        setattr(self, slug_field.attname, slug[:slug_len])
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        """Django meta class options.

        For more options:
        https://docs.djangoproject.com/en/1.11/ref/models/options/
        """

        abstract = True


class Channel(BaseModel):
    """Channel model.

    Sellers will publish their products in channels.
    """

    name = models.CharField(_('Name'), max_length=256, unique=True)

    class Meta:
        """Django meta class options.

        For more options:
        https://docs.djangoproject.com/en/1.11/ref/models/options/
        """

        ordering = ['name']
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        """Return the name attribute as representation."""
        return self.name


class Category(BaseModel, MPTTModel):
    """Category model.

    All published products need to be categorized
    in one of the channels' categories.
    """

    name = models.CharField(_('Name'), max_length=256)

    channel = models.ForeignKey(
        Channel,
        related_name='categories',
        verbose_name=_('Channel')
    )

    parent = TreeForeignKey(
        'self',
        related_name='children',
        blank=True,
        null=True,
        verbose_name=_('Parent')
    )

    slug_prefix = 'channel.reference'
    value_field_name = ('parent.reference', 'name',)

    class Meta:
        """Django meta class options.

        For more options:
        https://docs.djangoproject.com/en/1.11/ref/models/options/
        """

        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        unique_together = ('channel', 'name', 'parent',)

    def __str__(self):
        """Return the name attribute as representation."""
        return self.name
