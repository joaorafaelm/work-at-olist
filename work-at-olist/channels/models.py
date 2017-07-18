"""Models file.

All models of this module should be defined here.

"""

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """Abstract model for Channel and Category classes.

    Defines an abstract model built off of Django's Model class that
    provides some common fields that are useful on multiple models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField(_('Time created'), auto_now_add=True)
    time_modified = models.DateTimeField(_('Time modified'), auto_now=True)

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

    class Meta:
        """Django meta class options.

        For more options:
        https://docs.djangoproject.com/en/1.11/ref/models/options/
        """

        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        """Return the name attribute as representation."""
        return self.name
