from pydantic import BaseModel

from api.validation.base_rules import Rule


class Validator:
    def __init__(self, schema: BaseModel):
        self.schema: BaseModel = schema

    def rules(self) -> dict[str, list[Rule]]:
        raise NotImplementedError()

    def validate(self) -> None:
        for path, rules in self.rules().items():
            for rule in rules:
                rule.validate(self.schema)
