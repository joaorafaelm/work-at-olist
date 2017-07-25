"""Test file for the utils functions and classes."""

from channels.utils import Attrgetter
from django.test import TestCase


class TestUtils(TestCase):
    """Tests for the utils functions and classes."""

    def test_attrgetter(self):
        """Test if the Attrgetter class retrieves attributes correctly."""
        obj = type('Dummy', (object,), {'attr1': 'something', 'attr2': 322})
        self.assertEqual(Attrgetter('attr1')(obj), getattr(obj, 'attr1'))
        self.assertEqual(
            Attrgetter('attr1', 'attr2')(obj),
            tuple([
                getattr(obj, 'attr1'),
                getattr(obj, 'attr2')
            ])
        )
        with self.assertRaises(TypeError):
            Attrgetter({})(obj)
