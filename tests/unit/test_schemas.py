from datetime import datetime
from unittest import TestCase

from pydantic import BaseModel

from api.schemas import ItemBase, User, Product, ShoppingCart, ItemCreate, ItemUpdate, Item


class UserUnitTest(TestCase):
    def test_init(self) -> None:
        identifier = 1
        username = 'Mitko'
        password = 'TopSecretP@55'

        schema = User(id=identifier, username=username, password=password)
        self.assertIsInstance(schema, BaseModel)
        self.assertEqual(identifier, schema.id)
        self.assertEqual(username, schema.username)
        self.assertEqual(password, schema.password)


class ProductUnitTest(TestCase):
    def test_init(self) -> None:
        identifier = 1
        name = 'Computer'
        price = 123.45

        schema = Product(id=identifier, name=name, price=price)
        self.assertIsInstance(schema, BaseModel)
        self.assertEqual(identifier, schema.id)
        self.assertEqual(name, schema.name)
        self.assertEqual(price, schema.price)


class ShoppingCartUnitTest(TestCase):
    def test_init(self) -> None:
        identifier = 1
        user = User(id=1, username='Mitko', password='TopSecretP@55')
        expires_at = datetime(2024, 2, 1, 12, 34, 56)

        schema = ShoppingCart(id=identifier, user=user, expires_at=expires_at)
        self.assertIsInstance(schema, BaseModel)
        self.assertEqual(identifier, schema.id)
        self.assertEqual(user, schema.user)
        self.assertEqual(expires_at, schema.expires_at)


class ItemBaseUnitTest(TestCase):
    def test_init(self) -> None:
        schema = ItemBase()
        self.assertIsInstance(schema, BaseModel)


class ItemCreateUnitTest(TestCase):
    def test_init(self) -> None:
        product_id = 1
        product_name = 'Computer'

        schema = ItemCreate(product_id=product_id, product_name=product_name)
        self.assertIsInstance(schema, BaseModel)
        self.assertEqual(product_id, schema.product_id)
        self.assertEqual(product_name, schema.product_name)
        self.assertEqual(1, schema.quantity)

    def test_init_with_quantity(self) -> None:
        product_id = 1
        product_name = 'Computer'
        quantity = 13

        schema = ItemCreate(product_id=product_id, product_name=product_name, quantity=13)
        self.assertIsInstance(schema, ItemBase)
        self.assertEqual(product_id, schema.product_id)
        self.assertEqual(product_name, schema.product_name)
        self.assertEqual(quantity, schema.quantity)


class ItemUpdateUnitTest(TestCase):
    def test_init(self) -> None:
        quantity = 13

        schema = ItemUpdate(quantity=quantity)
        self.assertIsInstance(schema, ItemBase)
        self.assertEqual(quantity, schema.quantity)


class ItemUnitTest(TestCase):
    def test_init(self) -> None:
        identifier = 1
        shopping_cart_id = 2
        product = Product(id=3, name='Computer', price=123.45)
        quantity = 13
        reservation_identifier = 'reservation_identifier'

        schema = Item(
            id=identifier,
            shopping_cart_id=shopping_cart_id,
            product=product,
            quantity=quantity,
            reservation_identifier=reservation_identifier
        )
        self.assertIsInstance(schema, ItemBase)
        self.assertEqual(identifier, schema.id)
        self.assertEqual(shopping_cart_id, schema.shopping_cart_id)
        self.assertEqual(product, schema.product)
        self.assertEqual(quantity, schema.quantity)
        self.assertEqual(reservation_identifier, schema.reservation_identifier)
