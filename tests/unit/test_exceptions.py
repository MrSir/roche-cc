from unittest import TestCase

from api.exceptions import ObjectNotFoundError


class ObjectNotFoundErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = ObjectNotFoundError()

        self.assertIsInstance(exception, Exception)
