from __future__ import annotations

from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from pydantic import BaseModel

from api.database.models import Product
from api.exceptions import RequestValidationError, NullableValidationError
from api.validation.base_rules import Rule, RequiredRule, RequiredIfRule, NullableRule, IntegerRule, StringRule, \
    ExistsInRule, GreaterThanRule


class RuleTestSchema(BaseModel):
    name: str | None = 'Mitko'
    integer: int = 1


class RuleUnitTest(TestCase):
    def test_value(self) -> None:
        value = 'Mitko'

        rule = Rule()
        rule.path = 'name'
        rule.schema = RuleTestSchema(name=value)

        self.assertEqual(value, rule.value)

    def test_validate_raises_not_implemented_error(self) -> None:
        rule = Rule()

        with self.assertRaises(NotImplementedError):
            rule.validate()

    def test_fail_raises_not_implemented_error(self) -> None:
        rule = Rule()

        with self.assertRaises(NotImplementedError):
            rule.fail()


class RequiredRuleUnitTest(TestCase):
    def test_init(self) -> None:
        rule = RequiredRule()

        self.assertIsInstance(rule, Rule)

    def test_validate_passes(self) -> None:
        rule = RequiredRule()
        rule.path = 'name'
        rule.schema = RuleTestSchema()

        self.assertTrue(rule.validate())

    def test_validate_raises_request_validation_error(self) -> None:
        rule = RequiredRule()
        rule.path = 'name'
        rule.schema = RuleTestSchema(name=None)

        with self.assertRaises(RequestValidationError):
            rule.validate()

    def test_fail_raises_request_validation_error(self) -> None:
        path = 'name'

        rule = RequiredRule()
        rule.path = path

        with self.assertRaises(RequestValidationError) as mock_e:
            rule.fail()

        self.assertEqual(f'A value for "{path}" is required.', mock_e.exception.message)


class RequiredIfRuleUnitTest(TestCase):
    def test_init(self) -> None:
        rule = RequiredIfRule(True)

        self.assertIsInstance(rule, RequiredRule)

    def test_validate_passes(self) -> None:
        rule = RequiredIfRule(True)
        rule.path = 'name'
        rule.schema = RuleTestSchema()

        self.assertTrue(rule.validate())

    def test_validate_passes_when_condition_is_false(self) -> None:
        rule = RequiredIfRule(False)
        rule.path = 'name'
        rule.schema = RuleTestSchema(name=None)

        self.assertTrue(rule.validate())

    def test_validate_raises_request_validation_error(self) -> None:
        rule = RequiredIfRule(True)
        rule.path = 'name'
        rule.schema = RuleTestSchema(name=None)

        with self.assertRaises(RequestValidationError):
            rule.validate()

    def test_fail_raises_request_validation_error(self) -> None:
        path = 'name'

        rule = RequiredIfRule(True)
        rule.path = path

        with self.assertRaises(RequestValidationError) as mock_e:
            rule.fail()

        self.assertEqual(f'A value for "{path}" is required.', mock_e.exception.message)


class NullableRuleUnitTest(TestCase):
    def test_init(self) -> None:
        rule = NullableRule()

        self.assertIsInstance(rule, Rule)

    def test_validate_passes(self) -> None:
        rule = NullableRule()
        rule.path = 'name'
        rule.schema = RuleTestSchema()

        self.assertTrue(rule.validate())

    def test_validate_raises_nullable_validation_error(self) -> None:
        rule = NullableRule()
        rule.path = 'name'
        rule.schema = RuleTestSchema(name=None)

        with self.assertRaises(NullableValidationError):
            rule.validate()


class IntegerRuleUnitTest(TestCase):
    def test_init(self) -> None:
        rule = IntegerRule()

        self.assertIsInstance(rule, Rule)

    def test_validate_passes(self) -> None:
        rule = IntegerRule()
        rule.path = 'integer'
        rule.schema = RuleTestSchema()

        self.assertTrue(rule.validate())

    def test_validate_raises_request_validation_error(self) -> None:
        rule = IntegerRule()
        rule.path = 'name'
        rule.schema = RuleTestSchema()

        with self.assertRaises(RequestValidationError):
            rule.validate()

    def test_fail_raises_request_validation_error(self) -> None:
        path = 'name'

        rule = IntegerRule()
        rule.path = path

        with self.assertRaises(RequestValidationError) as mock_e:
            rule.fail()

        self.assertEqual(f'The value for "{path}" must be an integer.', mock_e.exception.message)


class StringRuleUnitTest(TestCase):
    def test_init(self) -> None:
        rule = StringRule()

        self.assertIsInstance(rule, Rule)

    def test_validate_passes(self) -> None:
        rule = StringRule()
        rule.path = 'name'
        rule.schema = RuleTestSchema()

        self.assertTrue(rule.validate())

    def test_validate_raises_request_validation_error(self) -> None:
        rule = StringRule()
        rule.path = 'integer'
        rule.schema = RuleTestSchema()

        with self.assertRaises(RequestValidationError):
            rule.validate()

    def test_fail_raises_request_validation_error(self) -> None:
        path = 'name'

        rule = StringRule()
        rule.path = path

        with self.assertRaises(RequestValidationError) as mock_e:
            rule.fail()

        self.assertEqual(f'The value for "{path}" must be a string.', mock_e.exception.message)


class ExistsInRuleUnitTest(TestCase):
    def test_init(self) -> None:
        rule = ExistsInRule(Product)

        self.assertIsInstance(rule, Rule)
        self.assertEqual(Product, rule.model)
        self.assertEqual('id', rule.column)

    def test_init_custom_column(self) -> None:
        column = 'name'
        rule = ExistsInRule(Product, column)

        self.assertIsInstance(rule, Rule)
        self.assertEqual(Product, rule.model)
        self.assertEqual(column, rule.column)

    def test_validate_passes(self) -> None:
        value = 2

        rule = ExistsInRule(Product)
        rule.path = 'integer'
        rule.schema = RuleTestSchema(integer=value)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_db_session)
        mock_db_session.filter = MagicMock(return_value=mock_db_session)
        mock_db_session.exists = MagicMock(return_value=mock_db_session)
        mock_db_session.scalar = MagicMock(return_value=True)

        with patch.object(rule, 'db_session', return_value=mock_db_session) as mock_dbs:
            self.assertTrue(rule.validate())

            mock_dbs.assert_called_once()
            mock_db_session.query.assert_has_calls(
                [
                    call(Product),
                    call(mock_db_session),
                ]
            )
            mock_db_session.filter.assert_called_once_with('id' == value)
            mock_db_session.exists.assert_called_once()
            mock_db_session.scalar.assert_called_once()

    def test_validate_raises_request_validation_error(self) -> None:
        value = 2

        rule = ExistsInRule(Product)
        rule.path = 'integer'
        rule.schema = RuleTestSchema(integer=value)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_db_session)
        mock_db_session.filter = MagicMock(return_value=mock_db_session)
        mock_db_session.exists = MagicMock(return_value=mock_db_session)
        mock_db_session.scalar = MagicMock(return_value=False)

        with patch.object(rule, 'db_session', return_value=mock_db_session) as mock_dbs:
            with self.assertRaises(RequestValidationError):
                rule.validate()

            mock_dbs.assert_called_once()
            mock_db_session.query.assert_has_calls(
                [
                    call(Product),
                    call(mock_db_session),
                ]
            )
            mock_db_session.filter.assert_called_once_with('id' == value)
            mock_db_session.exists.assert_called_once()
            mock_db_session.scalar.assert_called_once()

    def test_fail_raises_request_validation_error(self) -> None:
        path = 'name'

        rule = ExistsInRule(Product)
        rule.path = path

        with self.assertRaises(RequestValidationError) as mock_e:
            rule.fail()

        self.assertEqual(
            f'The value for "{path}" must exist in column "id" of model "{Product}".',
            mock_e.exception.message
        )


class GreaterThanRuleUnitTest(TestCase):
    def test_init(self) -> None:
        min_value = 0
        rule = GreaterThanRule(min_value)

        self.assertIsInstance(rule, Rule)
        self.assertEqual(min_value, rule.min_value)

    def test_validate_passes(self) -> None:
        rule = GreaterThanRule(0)
        rule.path = 'integer'
        rule.schema = RuleTestSchema()

        self.assertTrue(rule.validate())

    def test_validate_raises_request_validation_error(self) -> None:
        rule = GreaterThanRule(0)
        rule.path = 'integer'
        rule.schema = RuleTestSchema(integer=-1)

        with self.assertRaises(RequestValidationError):
            rule.validate()

    def test_fail_raises_request_validation_error(self) -> None:
        min_value = 0
        path = 'integer'

        rule = GreaterThanRule(min_value)
        rule.path = path

        with self.assertRaises(RequestValidationError) as mock_e:
            rule.fail()

        self.assertEqual(
            f'The value for "{path}" must be greater than "{min_value}".',
            mock_e.exception.message
        )
