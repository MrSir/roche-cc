from __future__ import annotations

from pydantic import BaseModel


class Rule:
    def validate(self, schema: BaseModel) -> bool:
        raise NotImplementedError()


class RequiredRule(Rule):
    def validate(self, schema: BaseModel) -> bool:
        # TODO implement
        return True


class RequiredIfRule(Rule):
    def __init__(self, condition: bool):
        self.condition = condition

    def validate(self, schema: BaseModel) -> bool:
        # TODO implement
        return True


class NullableRule(Rule):
    def validate(self, schema: BaseModel) -> bool:
        return True


class IntegerRule(Rule):
    def validate(self, schema: BaseModel) -> bool:
        return True


class StringRule(Rule):
    def validate(self, schema: BaseModel) -> bool:
        return True


class ExistsInRule(Rule):
    def __init__(self, table: str, column: str):
        self.table = table
        self.column = column

    def validate(self, schema: BaseModel) -> bool:
        return True


class GreaterThanRule(Rule):
    def __init__(self, min_value: int | float):
        self.min_value = min_value

    def validate(self, schema: BaseModel) -> bool:
        return True
