from __future__ import annotations

from unittest import TestCase

from api.database.models import Product
from api.schemas import ItemCreateSchema, ItemPartialUpdateSchema
from api.validation.base_rules import RequiredIfRule, NullableRule, IntegerRule, ExistsInRule, StringRule, \
    GreaterThanRule, RequiredRule
from api.validation.base_validators import Validator
from api.validation.items_validators import CreateItemValidator, PartialUpdateItemValidator


class CreateItemValidatorUnitTest(TestCase):
    def test_init(self) -> None:
        schema = ItemCreateSchema()
        validator = CreateItemValidator(schema)

        self.assertIsInstance(validator, Validator)

    def test_rules(self) -> None:
        schema = ItemCreateSchema()
        validator = CreateItemValidator(schema)

        self.assertIn('product_id', validator.rules())
        self.assertEqual(3, len(validator.rules()['product_id']))
        self.assertIsInstance(validator.rules()['product_id'][0], RequiredIfRule)
        self.assertIsInstance(validator.rules()['product_id'][1], IntegerRule)
        self.assertIsInstance(validator.rules()['product_id'][2], ExistsInRule)
        self.assertEqual(Product, getattr(validator.rules()['product_id'][2], 'model'))
        self.assertEqual('id', getattr(validator.rules()['product_id'][2], 'column'))

        self.assertIn('product_name', validator.rules())
        self.assertEqual(3, len(validator.rules()['product_name']))
        self.assertIsInstance(validator.rules()['product_name'][0], RequiredIfRule)
        self.assertIsInstance(validator.rules()['product_name'][1], StringRule)
        self.assertIsInstance(validator.rules()['product_name'][2], ExistsInRule)
        self.assertEqual(Product, getattr(validator.rules()['product_name'][2], 'model'))
        self.assertEqual('name', getattr(validator.rules()['product_name'][2], 'column'))

        self.assertIn('quantity', validator.rules())
        self.assertEqual(3, len(validator.rules()['quantity']))
        self.assertIsInstance(validator.rules()['quantity'][0], NullableRule)
        self.assertIsInstance(validator.rules()['quantity'][1], IntegerRule)
        self.assertIsInstance(validator.rules()['quantity'][2], GreaterThanRule)
        self.assertEqual(0, getattr(validator.rules()['quantity'][2], 'min_value'))


class PartialUpdateItemValidatorUnitTest(TestCase):
    def test_init(self) -> None:
        schema = ItemPartialUpdateSchema(quantity=2)
        validator = PartialUpdateItemValidator(schema)

        self.assertIsInstance(validator, Validator)

    def test_rules(self) -> None:
        schema = ItemPartialUpdateSchema(quantity=2)
        validator = PartialUpdateItemValidator(schema)

        self.assertIn('quantity', validator.rules())
        self.assertEqual(2, len(validator.rules()['quantity']))
        self.assertIsInstance(validator.rules()['quantity'][0], RequiredRule)
        self.assertIsInstance(validator.rules()['quantity'][1], GreaterThanRule)
        self.assertEqual(0, getattr(validator.rules()['quantity'][1], 'min_value'))
