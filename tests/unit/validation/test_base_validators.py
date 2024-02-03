from __future__ import annotations

from unittest import TestCase
from unittest.mock import patch, MagicMock

from pydantic import BaseModel

from api.exceptions import NullableValidationError
from api.validation.base_validators import Validator


class TestSchema(BaseModel):
    name: str | None = 'Mitko'


class ValidatorUnitTest(TestCase):
    def test_init(self) -> None:
        schema = TestSchema()
        validator = Validator(schema)

        self.assertEqual(schema, validator.schema)

    def test_rules_raises_not_implemented_error(self) -> None:
        schema = TestSchema()
        validator = Validator(schema)

        with self.assertRaises(NotImplementedError):
            validator.rules()

    def test_validate_iterates_over_rules(self) -> None:
        schema = TestSchema()
        validator = Validator(schema)

        rule1 = MagicMock()
        rule1.validate = MagicMock(return_value=True)

        rule2 = MagicMock()
        rule2.validate = MagicMock(return_value=True)

        rules = {
            'name': [rule1, rule2]
        }

        with patch.object(validator, 'rules', return_value=rules) as mock_r:
            validator.validate()

            mock_r.assert_called_once()
            rule1.validate.assert_called_once()
            rule2.validate.assert_called_once()

    def test_validate_skips_rules_when_nullable_validation_error(self) -> None:
        schema = TestSchema(name=None)
        validator = Validator(schema)

        rule1 = MagicMock()
        rule1.validate = MagicMock(side_effect=NullableValidationError())

        rule2 = MagicMock()
        rule2.validate = MagicMock(return_value=True)

        rules = {
            'name': [rule1, rule2]
        }

        with patch.object(validator, 'rules', return_value=rules) as mock_r:
            validator.validate()

            mock_r.assert_called_once()
            rule1.validate.assert_called_once()
            rule2.validate.assert_not_called()
