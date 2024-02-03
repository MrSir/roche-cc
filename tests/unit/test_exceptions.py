from unittest import TestCase

from api.exceptions import ObjectNotFoundError, RequestValidationError, NullableValidationError


class ObjectNotFoundErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = ObjectNotFoundError()

        self.assertIsInstance(exception, Exception)


class RequestValidationErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = RequestValidationError()

        self.assertIsInstance(exception, ValueError)


class NullableValidationErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = NullableValidationError()

        self.assertIsInstance(exception, ValueError)
