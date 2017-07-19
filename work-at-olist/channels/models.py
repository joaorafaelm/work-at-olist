"""Models file.

All models of this module should be defined here.

"""

import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """Abstract model for Channel and Category classes.

    Models that inherit from this class get an auto filled slug property
    based on the models name property (Along with created/updated time).

    Correctly truncates the field to the max_length of the slug field.

    The following attributes can be overridden on a per model basis:
    * value_field_name - the value to slugify, default 'name'
    * slug_field_name - the field to store the slugified value in,
                        default 'reference'.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField(_('Time created'), auto_now_add=True)
    time_modified = models.DateTimeField(_('Time modified'), auto_now=True)
    reference = models.SlugField(_('Reference'), max_length=100, unique=True)

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs):
        """Auto creates an slugified reference based on another attribute."""
        value_field_name = getattr(self, 'value_field_name', 'name')
        slug_field_name = getattr(self, 'slug_field_name', 'reference')

        # Retrieve the field where the slug will be stored
        slug_field = self._meta.get_field(slug_field_name)
        slug_len = slug_field.max_length

        # Slugify the field and make sure it is within the allowed length
        slug = slugify(getattr(self, value_field_name))

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


class Category(BaseModel):
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

    parent = models.ForeignKey(
        'self',
        related_name='children',
        blank=True,
        null=True,
        verbose_name=_('Parent')
    )

    reference = models.SlugField(_('Reference'), max_length=100)

    value_field_name = 'reference'

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
