from __future__ import annotations


class ObjectNotFoundError(Exception):
    def __init__(self, message: str | None = None, *args):
        self.message = message

        super().__init__(*args)


class UnauthorizedError(Exception):
    pass


class RequestValidationError(ValueError):
    def __init__(self, message: str | None = None, *args):
        self.message = message

        super().__init__(*args)


class NullableValidationError(ValueError):
    def __init__(self, message: str | None = None, *args):
        self.message = message

        super().__init__(*args)
