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
    quantity: int


class ItemCreate(ItemBase):
    product_id: int


class Item(ItemBase):
    id: int
    shopping_cart_id: int
    product: Product
    reserve_identifier: str | None = None

    class Config:
        orm_mode = True