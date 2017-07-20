"""This file contains the common used functions in the project."""


class Attrgetter:
    """Custom implementation of operator.attrgetter.

    Returns a list of attributes from an object. If the attribute is not found,
    returns an empty string.

    Usage: Attrgetter('person.name', 'person.id')(Person)

    The usage is the same as the builtin function:
    https://docs.python.org/3/library/operator.html#operator.attrgetter
    """

    __slots__ = ('_attrs', '_call')

    def __init__(self, attr, *attrs):
        """Create a callable func to retrieve the field(s) from the object."""
        if not attrs:
            if not isinstance(attr, str):
                raise TypeError('attribute name must be a string')
            self._attrs = (attr,)
            names = attr.split('.')

            def func(obj):
                for name in names:
                    obj = getattr(obj, name, '')
                return obj
            self._call = func
        else:
            self._attrs = (attr,) + attrs
            getters = tuple(map(Attrgetter, self._attrs))

            def func(obj):
                return tuple(getter(obj) for getter in getters)
            self._call = func

    def __call__(self, obj):
        """Return the callable created in the __init__ method."""
        return self._call(obj)

    def __repr__(self):
        """Define the objects representation."""
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__qualname__,
                              ', '.join(map(repr, self._attrs)))

    def __reduce__(self):
        """Define the type of the object.

        Url: https://docs.python.org/3/library/pickle.html#object.__reduce__
        """
        return self.__class__, self._attrs
