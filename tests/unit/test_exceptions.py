from unittest import TestCase

from api.exceptions import ObjectNotFoundError, RequestValidationError, NullableValidationError, UnauthorizedError


class ObjectNotFoundErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = ObjectNotFoundError()

        self.assertIsInstance(exception, Exception)


class UnauthorizedErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = UnauthorizedError()

        self.assertIsInstance(exception, Exception)


class RequestValidationErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = RequestValidationError()

        self.assertIsInstance(exception, ValueError)


class NullableValidationErrorUnitTest(TestCase):
    def test_init(self) -> None:
        exception = NullableValidationError()

        self.assertIsInstance(exception, ValueError)

