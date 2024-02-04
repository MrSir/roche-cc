from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from sqlalchemy.orm import Session

from api.controllers.base_controllers import AuthenticatedController, AuthorizedController, ValidatedController, \
    ResourcefulController, DBSessionController
from api.database.configuration import DBSession
from api.database.models import Item
from api.exceptions import RequestValidationError, ObjectNotFoundError


class AuthenticatedControllerUnitTest(TestCase):
    def test_init(self) -> None:
        db_session = DBSession()
        controller = AuthenticatedController(db_session)

        self.assertIsInstance(controller, DBSessionController)
        self.assertEqual(db_session, controller.db_session)


class AuthorizedControllerUnitTest(TestCase):
    def test_init(self) -> None:
        db_session = DBSession()
        controller = AuthorizedController(db_session)

        self.assertIsInstance(controller, AuthenticatedController)
        self.assertEqual(db_session, controller.db_session)

    def test_authorized_to_success(self) -> None:
        self.skipTest('AuthorizedController.authorized_to() functionality not yet implemented')

    def test_authorized_to_failure(self) -> None:
        self.skipTest('AuthorizedController.authorized_to() functionality not yet implemented')


class ValidatedControllerUnitTest(TestCase):
    def test_validate_to_success(self) -> None:
        validator = MagicMock()
        validator.validate = MagicMock(return_value=None)
        controller = ValidatedController()

        controller.validate(validator)
        validator.validate.assert_called_once()

    def test_validate_to_failure(self) -> None:
        validator = MagicMock()
        validator.validate = MagicMock(side_effect=RequestValidationError)
        controller = ValidatedController()

        with self.assertRaises(RequestValidationError) as mock_e:
            controller.validate(validator)

            validator.validate.assert_called_once()


class ResourcefulControllerUnitTest(TestCase):
    def test_init(self) -> None:
        db_session = DBSession()
        controller = ResourcefulController(db_session)
        controller.model_class = Item

        self.assertIsInstance(controller, DBSessionController)
        self.assertEqual(db_session, controller.db_session)
        self.assertTrue(hasattr(controller, 'model_class'))

    def test_get_object_returns_instance(self) -> None:
        identifier = 1
        item = Item(id=identifier)

        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        mock_query.first = MagicMock(return_value=item)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_query)

        controller = ResourcefulController(mock_db_session)
        controller.model_class = Item

        self.assertEqual(item, controller.get_object(identifier))

        mock_db_session.query.assert_called_once_with(Item)
        mock_query.filter.assert_called_once()
        mock_query.first.assert_called_once()

    def test_get_object_raises_object_not_found_error(self) -> None:
        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        mock_query.first = MagicMock(return_value=None)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_query)

        controller = ResourcefulController(mock_db_session)
        controller.model_class = Item

        identifier = 1
        item = Item(id=identifier)

        with self.assertRaises(ObjectNotFoundError) as mock_e:
            self.assertEqual(item, controller.get_object(identifier))

            mock_db_session.query.assert_called_once_with(Item)
            mock_query.filter.assert_called_once()
            mock_query.first.assert_called_once()
