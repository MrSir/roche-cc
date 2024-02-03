from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from api.controllers.items_controller import ItemsController
from api.database.models import User, Item, ShoppingCart
from api.schemas import ItemCreateSchema
from api.validation.items_validators import CreateItemValidator


class ItemsControllerIntegrationTest(TestCase):
    @patch('api.controllers.items_controller.ItemsController.db_session', new_callable=PropertyMock())
    @patch('api.controllers.items_controller.ItemsController.user', new_callable=PropertyMock())
    def test_index(self, mock_db_session, mock_user) -> None:
        controller = ItemsController()

        mock_user.id.return_value = 1

        mock_query = MagicMock()
        mock_query.join = MagicMock(return_value=mock_query)
        mock_query.filter = MagicMock(return_value=mock_query)
        mock_query.join = MagicMock(return_value=mock_query)
        mock_db_session.query = MagicMock(return_value=mock_query)

        mock_authorized_to = MagicMock(return_value=None)

        with patch.multiple(
            controller,
            user=mock_user,
            authorized_to=mock_authorized_to,
            db_session=mock_db_session
        ) as mocks:
            controller.index()

            mock_authorized_to.assert_called_once_with('index_items')
            mock_db_session.query.assert_called_once_with(Item)
            mock_query.join.assert_called_once_with(ShoppingCart)
            self.assertEqual(2, mock_query.filter.call_count)

        for mock in mocks:
            mock.asssert_called_once()

    def test_create(self) -> None:
        product_id = 1
        quantity = 2

        controller = ItemsController()
        schema = ItemCreateSchema(product_id=product_id, quantity=quantity)

        mock_authorized_to = MagicMock(return_value=controller)
        mock_validate = MagicMock(return_value=controller)
        mock_shopping_cart_service = MagicMock()
        mock_shopping_cart_service.add_item = MagicMock()

        with patch.multiple(
            controller,
            authorized_to=mock_authorized_to,
            validate=mock_validate,
            shopping_cart_service=mock_shopping_cart_service
        ) as mocks:
            controller.create(schema)

            mock_authorized_to.assert_called_once_with('create_item')
            mock_validate.assert_called_once_with(CreateItemValidator(schema))
            mock_shopping_cart_service.add_item.assert_called_once_with(product_id, quantity)
