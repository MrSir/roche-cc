from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str


class Product(BaseModel):
    id: int
    name: str
    price: float


class ShoppingCart(BaseModel):
    id: int
    user: User
    expires_at: datetime


class ItemBase(BaseModel):
    pass


class ItemCreate(ItemBase):
    product_id: int | None = None
    product_name: str | None = None
    quantity: int | None = 1


class ItemUpdate(ItemBase):
    quantity: int


class Item(ItemBase):
    id: int
    shopping_cart_id: int
    product: Product
    quantity: int
    reservation_identifier: str | None = None

    class Config:
        from_attributes = True
