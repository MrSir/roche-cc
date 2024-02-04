from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from api.controllers.items_controller import ItemsController
from api.database.models import User, Item, ShoppingCart, Product
from api.schemas import ItemCreateSchema, ItemPartialUpdateSchema


class ItemsControllerIntegrationTest(TestCase):
    def test_index(self) -> None:
        mock_query = MagicMock()
        mock_query.join = MagicMock(return_value=mock_query)
        mock_query.filter = MagicMock(return_value=mock_query)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_query)

        controller = ItemsController(mock_db_session)
        controller._user = User(id=1)

        with patch.object(controller, 'authorized_to', return_value=None) as mock_authorized_to:
            controller.index()

        mock_authorized_to.assert_called_once_with('index_items')
        mock_db_session.query.assert_called_once_with(Item)
        mock_query.join.assert_called_once_with(ShoppingCart)

        self.assertEqual(2, mock_query.filter.call_count)

    @patch('api.controllers.items_controller.CreateItemValidator.validate')
    def test_create(self, mock_validator_validate) -> None:
        product_id = 1
        quantity = 2

        item = Item(id=1, product_id=product_id, quantity=quantity)

        mock_db_session = MagicMock()
        controller = ItemsController(mock_db_session)
        schema = ItemCreateSchema(product_id=product_id, quantity=quantity)

        mock_authorized_to = MagicMock(return_value=controller)
        mock_shopping_cart_service = MagicMock()
        mock_shopping_cart_service.for_user = MagicMock(return_value=mock_shopping_cart_service)
        mock_shopping_cart_service.add_item = MagicMock(return_value=item)

        with patch.multiple(
            controller,
            authorized_to=mock_authorized_to,
            shopping_cart_service=mock_shopping_cart_service
        ) as mocks:
            self.assertEqual(item, controller.create(schema))

            mock_authorized_to.assert_called_once_with('create_item')
            mock_validator_validate.assert_called_once()
            mock_shopping_cart_service.add_item.assert_called_once_with(product_id, quantity)

    @patch('api.controllers.items_controller.CreateItemValidator.validate')
    def test_create_resolves_product_id_from_product_name(self, mock_validator_validate) -> None:
        product_id = 2
        product_name = 'Computer'
        quantity = 2

        item = Item(id=1, product_id=product_id, quantity=quantity)

        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        mock_query.first = MagicMock(return_value=Product(id=product_id))

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_query)

        controller = ItemsController(mock_db_session)
        schema = ItemCreateSchema(product_name=product_name, quantity=quantity)

        mock_authorized_to = MagicMock(return_value=controller)
        mock_shopping_cart_service = MagicMock()
        mock_shopping_cart_service.for_user = MagicMock(return_value=mock_shopping_cart_service)
        mock_shopping_cart_service.add_item = MagicMock(return_value=item)

        with patch.multiple(
                controller,
                authorized_to=mock_authorized_to,
                shopping_cart_service=mock_shopping_cart_service
        ) as mocks:
            self.assertEqual(item, controller.create(schema))

            mock_authorized_to.assert_called_once_with('create_item')
            mock_validator_validate.assert_called_once()
            mock_shopping_cart_service.add_item.assert_called_once_with(product_id, quantity)

        for mock in mocks:
            mock.assert_called_once()

    @patch('api.controllers.items_controller.PartialUpdateItemValidator.validate')
    def test_partial_update(self, mock_validator_validate) -> None:
        product_id = 1
        quantity = 2
        item = Item(id=1, product_id=product_id, quantity=quantity)

        mock_db_session = MagicMock()
        controller = ItemsController(mock_db_session)
        schema = ItemPartialUpdateSchema(quantity=quantity)

        mock_authorized_to = MagicMock(return_value=controller)
        mock_shopping_cart_service = MagicMock()
        mock_shopping_cart_service.for_user = MagicMock(return_value=mock_shopping_cart_service)
        mock_shopping_cart_service.update_quantity = MagicMock(return_value=item)

        with patch.multiple(
                controller,
                get_object=MagicMock(return_value=item),
                authorized_to=mock_authorized_to,
                shopping_cart_service=mock_shopping_cart_service
        ) as mocks:
            self.assertEqual(item, controller.partial_update(item.id, schema))

            mock_authorized_to.assert_called_once_with('update_item')
            mock_validator_validate.assert_called_once()
            mock_shopping_cart_service.update_quantity.assert_called_once_with(item, quantity)

        for mock in mocks:
            mock.assert_called_once()

    def test_delete(self) -> None:
        product_id = 1
        quantity = 2
        item = Item(id=1, product_id=product_id, quantity=quantity)

        mock_db_session = MagicMock()
        controller = ItemsController(mock_db_session)

        mock_authorized_to = MagicMock(return_value=controller)
        mock_shopping_cart_service = MagicMock()
        mock_shopping_cart_service.for_user = MagicMock(return_value=mock_shopping_cart_service)
        mock_shopping_cart_service.remove_item = MagicMock(return_value=None)

        with patch.multiple(
                controller,
                get_object=MagicMock(return_value=item),
                authorized_to=mock_authorized_to,
                shopping_cart_service=mock_shopping_cart_service
        ) as mocks:
            self.assertIsNone(controller.delete(item.id))

            mock_authorized_to.assert_called_once_with('delete_item')
            mock_shopping_cart_service.remove_item.assert_called_once_with(item)

        for mock in mocks:
            mock.assert_called_once()
