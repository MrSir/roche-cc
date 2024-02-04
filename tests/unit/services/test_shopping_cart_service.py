from unittest import TestCase
from unittest.mock import MagicMock, patch

import arrow

from api.database.models import User, ShoppingCart, Item
from api.services.shopping_cart_service import ShoppingCartService


class ShoppingCartServiceUnitTest(TestCase):
    def test_init(self) -> None:
        db_session = MagicMock()
        service = ShoppingCartService(db_session)

        self.assertEqual(db_session, service.db_session)
        self.assertIsNone(service._shopping_cart)

    def test_shopping_cart_returns_preset(self) -> None:
        db_session = MagicMock()
        shopping_cart = ShoppingCart(id=2)

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        self.assertEqual(shopping_cart, service.shopping_cart)

    def test_shopping_cart_retrieves_existing(self) -> None:
        user = User(id=1)
        expires_at = arrow.now().shift(minutes=30)

        db_session = MagicMock()

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)

        service = ShoppingCartService(db_session)
        service.for_user(user)

        with patch.multiple(
                service,
                new_expiry=MagicMock(return_value=expires_at),
                find_shopping_cart=MagicMock(return_value=shopping_cart)
        ) as mocks:
            self.assertEqual(shopping_cart.user, service.shopping_cart.user)
            self.assertEqual(shopping_cart.expires_at, service.shopping_cart.expires_at)

        for mock in mocks:
            mock.assert_called_once()

    def test_shopping_cart_gets_created(self) -> None:
        user = User(id=1)
        expires_at = arrow.now().shift(minutes=30)

        db_session = MagicMock()

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)

        service = ShoppingCartService(db_session)
        service.for_user(user)

        with patch.multiple(
                service,
                new_expiry=MagicMock(return_value=expires_at),
                find_shopping_cart=MagicMock(return_value=None),
                create_shopping_cart=MagicMock(return_value=shopping_cart)
        ) as mocks:
            self.assertEqual(shopping_cart, service.shopping_cart)

        for mock in mocks:
            mock.assert_called_once()

    def test_find_shopping_cart(self) -> None:
        user = User(id=1)
        expires_at = arrow.now().shift(minutes=30)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)

        db_session = MagicMock()
        db_session.query = MagicMock(return_value=db_session)
        db_session.filter = MagicMock(return_value=db_session)
        db_session.first = MagicMock(return_value=shopping_cart)

        service = ShoppingCartService(db_session)

        self.assertEqual(shopping_cart, service.for_user(user).find_shopping_cart())

    def test_create_shopping_cart(self) -> None:
        user = User(id=1)
        expires_at = arrow.now().shift(minutes=30)

        db_session = MagicMock()
        db_session.add = MagicMock(return_value=db_session)
        db_session.commit = MagicMock(return_value=None)
        db_session.refresh = MagicMock(return_value=None)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)

        service = ShoppingCartService(db_session)

        with patch.object(service, 'new_expiry', return_value=expires_at) as mock_new_expiry:
            actual_shopping_cart = service.for_user(user).create_shopping_cart()

        mock_new_expiry.assert_called_once()

        self.assertEqual(shopping_cart.user, actual_shopping_cart.user)
        self.assertEqual(shopping_cart.expires_at, actual_shopping_cart.expires_at)
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_delete_shopping_cart(self) -> None:
        user = User(id=1)
        db_session = MagicMock()
        db_session.delete = MagicMock(return_value=db_session)
        db_session.commit = MagicMock(return_value=None)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=arrow.now().shift(minutes=30))

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        service.delete_shopping_cart()

        self.assertIsNone(service._shopping_cart)
        db_session.delete.assert_called_once_with(shopping_cart)
        db_session.commit.assert_called_once()

    def test_increase_expiry_shopping_cart(self) -> None:
        user = User(id=1)
        expires_at = arrow.now().shift(minutes=30)

        db_session = MagicMock()
        db_session.query = MagicMock(return_value=db_session)
        db_session.filter = MagicMock(return_value=db_session)
        db_session.update = MagicMock(return_value=None)
        db_session.commit = MagicMock(return_value=None)
        db_session.refresh = MagicMock(return_value=None)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        with patch.object(service, 'new_expiry', return_value=expires_at) as mock_new_expiry:
            service.increase_expiry_of_shopping_cart()

        mock_new_expiry.assert_called_once()

        db_session.query.assert_called_once_with(ShoppingCart)
        db_session.filter.assert_called_once()
        db_session.update.assert_called_once_with({
            ShoppingCart.expires_at: expires_at
        })
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_add_item_updates_existing(self) -> None:
        product_id = 2
        quantity = 2
        user = User(id=1)

        expires_at = arrow.now().shift(minutes=30)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)
        item = Item(id=1, shopping_cart=shopping_cart, product_id=product_id, quantity=1)

        db_session = MagicMock()
        db_session.query = MagicMock(return_value=db_session)
        db_session.filter = MagicMock(return_value=db_session)
        db_session.first = MagicMock(return_value=item)

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        with patch.object(service, 'update_quantity', return_value=item) as mock_uq:
            self.assertEqual(item, service.for_user(user).add_item(product_id, quantity))

        mock_uq.assert_called_once()

        db_session.query.assert_called_once_with(Item)
        self.assertEqual(2, db_session.filter.call_count)
        db_session.first.assert_called_once()

    @patch('api.services.shopping_cart_service.ReserveItemJob.queue')
    def test_add_item(self, mock_queue) -> None:
        product_id = 2
        quantity = 2
        user = User(id=1)

        expires_at = arrow.now().shift(minutes=30)

        db_session = MagicMock()
        db_session.query = MagicMock(return_value=db_session)
        db_session.filter = MagicMock(return_value=db_session)
        db_session.first = MagicMock(return_value=None)
        db_session.add = MagicMock(return_value=db_session)
        db_session.commit = MagicMock(return_value=None)
        db_session.refresh = MagicMock(return_value=None)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=expires_at)

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        with patch.multiple(
                service,
                increase_expiry_of_shopping_cart=MagicMock(return_value=None),
                new_expiry=MagicMock(return_value=expires_at)
        ) as mocks:
            self.assertIsInstance(service.for_user(user).add_item(product_id, quantity), Item)

        for mock in mocks:
            mock.assert_called_once()

        db_session.query.assert_called_once_with(Item)
        self.assertEqual(2, db_session.filter.call_count)
        db_session.first.assert_called_once()
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

        mock_queue.assert_called_once()

    @patch('api.services.shopping_cart_service.ReserveItemJob.queue')
    def test_update_quantity(self, mock_queue) -> None:
        product_id = 2
        quantity = 2
        user = User(id=1)
        item = Item(id=2, product_id=product_id, quantity=1)

        db_session = MagicMock()
        db_session.query = MagicMock(return_value=db_session)
        db_session.filter = MagicMock(return_value=db_session)
        db_session.update = MagicMock(return_value=db_session)
        db_session.commit = MagicMock(return_value=None)
        db_session.refresh = MagicMock(return_value=None)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=arrow.now().shift(minutes=30))

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        with patch.object(service, 'increase_expiry_of_shopping_cart', return_value=None) as mock_ieosc:
            self.assertIsInstance(service.update_quantity(item, quantity), Item)

        mock_ieosc.assert_called_once()

        db_session.query.assert_called_once_with(Item)
        db_session.filter.assert_called_once()
        db_session.update.assert_called_once_with({Item.quantity: quantity})
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

        mock_queue.assert_called_once()

    @patch('api.services.shopping_cart_service.ReleaseReservedItemJob.queue')
    def test_remove_item(self, mock_queue) -> None:
        product_id = 2
        user = User(id=1)
        item = Item(id=2, product_id=product_id, quantity=1)

        db_session = MagicMock()
        db_session.query = MagicMock(return_value=db_session)
        db_session.filter = MagicMock(return_value=db_session)
        db_session.update = MagicMock(return_value=db_session)
        db_session.commit = MagicMock(return_value=None)
        db_session.refresh = MagicMock(return_value=None)

        shopping_cart = ShoppingCart(id=2, user=user, expires_at=arrow.now().shift(minutes=30))

        service = ShoppingCartService(db_session)
        service._shopping_cart = shopping_cart

        with patch.object(service, 'increase_expiry_of_shopping_cart', return_value=None) as mock_ieosc:
            service.remove_item(item)

        mock_ieosc.assert_called_once()

        db_session.query.assert_called_once_with(Item)
        db_session.filter.assert_called_once()
        db_session.update.assert_called_once_with({Item.quantity: 0})
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

        mock_queue.assert_called_once()
