from fastapi import APIRouter
from sqlalchemy.orm import Session

from api.controllers.base_controllers import AuthenticatedController
from api.database import models
from api import schemas


class ItemsController(AuthenticatedController):
    def __init__(self, db_session: Session):
        self.name = 'Items'

        self.db_session = db_session
        self.router = APIRouter(tags=['Items'])
        self.router.add_api_route("/items", self.index, methods=["GET"])
        self.router.add_api_route("/items", self.create, methods=["POST"])

        # Bonus
        self.router.add_api_route("/items/{item_id}", self.update, methods=["PUT"])
        self.router.add_api_route("/items/{item_id}", self.delete, methods=["DELETE"])

    def index(self) -> list[schemas.Item]:
        return self.db_session.query(models.Item).filter(models.ShoppingCart.user_id == self.user().id)

    def create(self, item: schemas.ItemCreate) -> schemas.Item:
        pass

    def update(self, item_id: int, item: schemas.ItemBase) -> schemas.Item:
        pass

    def delete(self, item_id: int) -> None:
        pass

