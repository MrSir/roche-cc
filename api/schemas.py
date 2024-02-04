from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    password: str


class ProductSchema(BaseModel):
    id: int
    name: str
    price: float


class ShoppingCartSchema(BaseModel):
    id: int
    user: UserSchema
    expires_at: datetime


class ItemBaseSchema(BaseModel):
    pass


class ItemCreateSchema(ItemBaseSchema):
    product_id: int | None = None
    product_name: str | None = None
    quantity: int | None = 1


class ItemPartialUpdateSchema(ItemBaseSchema):
    quantity: int


class ItemSchema(ItemBaseSchema):
    id: int
    shopping_cart_id: int
    product: ProductSchema
    quantity: int
    reservation_identifier: str | None = None

    class Config:
        from_attributes = True
