from __future__ import annotations

from functools import cached_property
from typing import Any, Type

from pydantic import BaseModel

from api.database.configuration import Base, DBSession

from api.exceptions import RequestValidationError, NullableValidationError


class Rule:
    path: str
    schema: BaseModel

    @cached_property
    def value(self) -> Any:
        return getattr(self.schema, self.path)

    def validate(self) -> bool:
        raise NotImplementedError()

    def fail(self) -> None:
        raise NotImplementedError()


class RequiredRule(Rule):
    def validate(self) -> bool:
        if self.value is None:
            self.fail()

        return True

    def fail(self) -> None:
        message = f'A value for "{self.path}" is required.'

        raise RequestValidationError(message)


class RequiredIfRule(RequiredRule):
    def __init__(self, condition: bool):
        self.condition = condition

        super().__init__()

    def validate(self) -> bool:
        if self.condition:
            if self.value is None:
                self.fail()

        return True


class NullableRule(Rule):
    def validate(self) -> bool:
        if self.value is None:
            self.skip_following_rules()

        return True

    def skip_following_rules(self) -> None:
        raise NullableValidationError()

    def fail(self) -> None:
        pass


class IntegerRule(Rule):
    def validate(self) -> bool:
        if type(self.value) is not int:
            self.fail()

        return True

    def fail(self) -> None:
        message = f'The value for "{self.path}" must be an integer.'

        raise RequestValidationError(message)


class StringRule(Rule):
    def validate(self) -> bool:
        if type(self.value) is not str:
            self.fail()

        return True

    def fail(self) -> None:
        message = f'The value for "{self.path}" must be a string.'

        raise RequestValidationError(message)


class ExistsInRule(Rule):
    def __init__(self, model: Type[Base], column: str = 'id'):
        self.model = model
        self.column = column

        super().__init__()

    def db_session(self) -> DBSession:
        return DBSession()

    def validate(self) -> bool:
        db_session = self.db_session()

        result = (
            db_session.query(
                db_session.query(self.model).filter(self.column == self.value).exists()
            ).scalar()
        )

        if result is False:
            self.fail()

        return True

    def fail(self) -> None:
        message = f'The value for "{self.path}" must exist in column "{self.column}" of model "{self.model}".'

        raise RequestValidationError(message)


class GreaterThanRule(Rule):
    def __init__(self, min_value: int | float):
        self.min_value = min_value

        super().__init__()

    def validate(self) -> bool:
        if self.value < self.min_value:
            self.fail()

        return True

    def fail(self) -> None:
        message = f'The value for "{self.path}" must be greater than "{self.min_value}".'

        raise RequestValidationError(message)
