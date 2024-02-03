from unittest import TestCase

from fastapi import APIRouter
from fastapi.routing import APIRoute

from api.controllers.base_controllers import AuthorizedController, ValidatedController, ResourcefulController
from api.controllers.items_controller import ItemsController
from api.services.shopping_cart_service import ShoppingCartService


class ItemsControllerUnitTest(TestCase):
    def test_init(self) -> None:
        controller = ItemsController()

        self.assertIsInstance(controller, AuthorizedController)
        self.assertIsInstance(controller, ValidatedController)
        self.assertIsInstance(controller, ResourcefulController)

        self.assertIsInstance(controller.router, APIRouter)
        self.assertEqual(['Items'], controller.router.tags)

        self.assertEqual(4, len(controller.router.routes))
        self.assertIsInstance(controller.router.routes[0], APIRoute)
        self.assertEqual('/items', controller.router.routes[0].path)
        self.assertEqual('index', controller.router.routes[0].name)
        self.assertEqual({'GET'}, controller.router.routes[0].methods)
        self.assertIsInstance(controller.router.routes[1], APIRoute)
        self.assertEqual('/items', controller.router.routes[1].path)
        self.assertEqual('create', controller.router.routes[1].name)
        self.assertEqual({'POST'}, controller.router.routes[1].methods)
        self.assertIsInstance(controller.router.routes[2], APIRoute)
        self.assertEqual('/items/{item_id}', controller.router.routes[2].path)
        self.assertEqual('partial_update', controller.router.routes[2].name)
        self.assertEqual({'PATCH'}, controller.router.routes[2].methods)
        self.assertIsInstance(controller.router.routes[3], APIRoute)
        self.assertEqual('/items/{item_id}', controller.router.routes[3].path)
        self.assertEqual('delete', controller.router.routes[3].name)
        self.assertEqual({'DELETE'}, controller.router.routes[3].methods)

        self.assertIsInstance(controller.shopping_cart_service, ShoppingCartService)

