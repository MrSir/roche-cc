from __future__ import annotations

import arrow
from sqlalchemy.orm import Session

from api.database.models import User, ShoppingCart, Item
from api.jobs.reservation_jobs import ReserveItemJob, ReleaseReservedItemJob


class ShoppingCartService:
    user: User

    def __init__(self, db_session: Session):
        self.db_session: Session = db_session
        self._shopping_cart: ShoppingCart | None = None

    def for_user(self, user: User) -> ShoppingCartService:
        self.user = user

        return self

    @property
    def shopping_cart(self) -> ShoppingCart:
        if self._shopping_cart is None:
            self._shopping_cart = self.find_shopping_cart()

            if self._shopping_cart is None:
                self._shopping_cart = self.create_shopping_cart()

        return self._shopping_cart

    def new_expiry(self) -> arrow:
        return arrow.now().shift(minutes=30)

    def find_shopping_cart(self) -> ShoppingCart:
        return self.db_session.query(ShoppingCart).filter(ShoppingCart.user == self.user).first()

    def create_shopping_cart(self) -> ShoppingCart:
        shopping_cart = ShoppingCart(user=self.user, expires_at=self.new_expiry().datetime)
        self.db_session.add(shopping_cart)
        self.db_session.commit()
        self.db_session.refresh(shopping_cart)

        return shopping_cart

    def delete_shopping_cart(self) -> None:
        self.db_session.delete(self.shopping_cart)
        self.db_session.commit()

        self._shopping_cart = None

    def increase_expiry_of_shopping_cart(self) -> None:
        self.db_session.query(ShoppingCart).filter(ShoppingCart.id == self.shopping_cart.id).update({
            ShoppingCart.expires_at: self.new_expiry().datetime
        })

        self.db_session.commit()
        self.db_session.refresh(self._shopping_cart)

    def add_item(self, product_id: int, quantity: int) -> Item:
        item = (
            self.db_session.query(Item)
                .filter(Item.shopping_cart == self.shopping_cart)
                .filter(Item.product_id == product_id)
                .first()
        )

        if item is not None:
            return self.update_quantity(item, item.quantity + quantity)

        item = Item(shopping_cart=self.shopping_cart, product_id=product_id, quantity=quantity)
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)

        # Update the current instance of the shopping cart
        self.increase_expiry_of_shopping_cart()

        # Queue reservation async job
        ReserveItemJob(item.id).queue()

        return item

    def update_quantity(self, item: Item, quantity: int) -> Item | None:
        self.db_session.query(Item).filter(Item.id == item.id).update({Item.quantity: quantity})

        self.db_session.commit()
        self.db_session.refresh(item)

        # Update the current instance of the shopping cart
        self.increase_expiry_of_shopping_cart()

        # Queue reservation async job
        ReserveItemJob(item.id).queue()

        return item

    def remove_item(self, item: Item) -> None:
        self.db_session.query(Item).filter(Item.id == item.id).update({Item.quantity: 0})
        self.db_session.commit()
        self.db_session.refresh(item)

        # Update the current instance of the shopping cart
        self.increase_expiry_of_shopping_cart()

        # Queue reservation release async job
        ReleaseReservedItemJob(item.id).queue()
