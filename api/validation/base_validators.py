from pydantic import BaseModel

from api.exceptions import NullableValidationError, RequestValidationError
from api.validation.base_rules import Rule


class Validator:
    def __init__(self, schema: BaseModel):
        self.schema: BaseModel = schema

    def rules(self) -> dict[str, list[Rule]]:
        raise NotImplementedError()

    def validate(self) -> None:
        for path, rules in self.rules().items():
            for rule in rules:
                rule.path = path
                rule.schema = self.schema

                try:
                    rule.validate()
                except RequestValidationError as e:
                    print(e.message)
                except NullableValidationError:
                    # If the value is null and has a nullable rule in front it should skip the rest of the rules
                    break
