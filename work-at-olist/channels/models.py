"""Models file.

All models of this module should be defined here.

"""

import uuid

from django.db import IntegrityError, models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """Abstract model for Channel and Category classes.

    Models that inherit from this class get an auto filled slug property
    based on the models name property (Along with created/updated time).

    Correctly handles duplicate values (slugs are unique), and truncates slug
    if value is too long (max_length is 100 by default).

    The following attributes can be overridden on a per model basis:
    * value_field_name - the value to slugify, default 'name'
    * slug_field_name - the field to store the slugified value in,
                        default 'reference'.
    * max_interations - how many iterations to search for an open slug before
                        raising IntegrityError, default 1000.
    * slug_separator - the character to put in place of spaces and other non
                       url friendly characters, default '-'.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField(_('Time created'), auto_now_add=True)
    time_modified = models.DateTimeField(_('Time modified'), auto_now=True)
    reference = models.SlugField(_('Reference'), max_length=100, unique=True)

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs):
        """Auto creates an slugified reference based on another attribute."""
        pk_field_name = self._meta.pk.name
        value_field_name = getattr(self, 'value_field_name', 'name')
        slug_field_name = getattr(self, 'slug_field_name', 'reference')
        max_interations = getattr(self, 'slug_max_iterations', 1000)
        slug_separator = getattr(self, 'slug_separator', '-')

        # fields, query set, other setup variables
        slug_field = self._meta.get_field(slug_field_name)
        slug_len = slug_field.max_length
        queryset = self.__class__.objects.all()

        # if the pk of the record is set, exclude it from the slug search
        current_pk = getattr(self, pk_field_name)
        if current_pk:
            queryset = queryset.exclude(**{pk_field_name: current_pk})

        # setup the original slug,
        # and make sure it is within the allowed length
        slug = slugify(getattr(self, value_field_name))
        if slug_len:
            slug = slug[:slug_len]
        original_slug = slug

        # iterate until a unique slug is found, or max_iterations
        counter = 2
        while queryset.filter(**{
            slug_field_name: slug
        }).count() > 0 and counter < max_interations:
            slug = original_slug
            suffix = '%s%s' % (slug_separator, counter)
            if slug_len and len(slug) + len(suffix) > slug_len:
                slug = slug[:slug_len - len(suffix)]
            slug = '%s%s' % (slug, suffix)
            counter += 1

        if counter == max_interations:
            raise IntegrityError('Unable to locate unique slug.')

        setattr(self, slug_field.attname, slug)

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
