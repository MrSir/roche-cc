from __future__ import annotations

from fastapi import APIRouter

from api.controllers.base_controllers import AuthorizedController, ValidatedController, ResourcefulController
from api.database.models import Item, ShoppingCart, Product
from api.schemas import ItemSchema, ItemCreateSchema, ItemPartialUpdateSchema
from api.services.shopping_cart_service import ShoppingCartService
from api.validation.items_validators import PartialUpdateItemValidator, CreateItemValidator


class ItemsController(AuthorizedController, ValidatedController, ResourcefulController):
    model_class = Item

    def __init__(self):
        self.router = APIRouter(tags=['Items'])
        self.router.add_api_route("/items", self.index, methods=["GET"])
        self.router.add_api_route("/items", self.create, methods=["POST"])

        # Bonus
        self.router.add_api_route("/items/{item_id}", self.partial_update, methods=["PATCH"])
        self.router.add_api_route("/items/{item_id}", self.delete, methods=["DELETE"])

        super().__init__()

        self.shopping_cart_service = ShoppingCartService(self.user, self.db_session)

    def index(self) -> list[ItemSchema]:
        self.authorized_to('index_items')

        items = (
            self.db_session
                .query(Item)
                .join(ShoppingCart)
                .filter(ShoppingCart.user_id == self.user.id)
                .filter(Item.quantity != 0)
        )

        # TODO: implement proper formatting for response

        return items

    def create(self, schema: ItemCreateSchema) -> ItemSchema:
        self.authorized_to('create_item').validate(CreateItemValidator(schema))

        product_id = schema.product_id

        # Resolve product_id if not provided
        if product_id is None:
            product = self.db_session.query(Product).filter(Product.name == schema.product_name).first()
            product_id = product.id

        item = self.shopping_cart_service.add_item(product_id, schema.quantity)

        # TODO: implement proper formatting for response

        return item

    #### Bonus ####
    def partial_update(self, item_id: int, schema: ItemPartialUpdateSchema) -> ItemSchema | None:
        self.authorized_to('update_item').validate(PartialUpdateItemValidator(schema))

        item = self.shopping_cart_service.update_quantity(self.get_object(item_id), schema.quantity)

        # TODO: implement proper formatting for response

        return item

    def delete(self, item_id: int) -> None:
        self.authorized_to('delete_item')

        item = self.shopping_cart_service.update_quantity(self.get_object(item_id), 0)

        # TODO: implement proper formatting for response

        return item
