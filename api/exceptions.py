class ObjectNotFoundError(Exception):
    pass


class RequestValidationError(ValueError):
    pass


class NullableValidationError(ValueError):
    pass
