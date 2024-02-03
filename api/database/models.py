from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from api.database.configuration import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    shopping_cart = relationship('ShoppingCart', back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    price = Column(DECIMAL)


class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    expires_at = Column(DateTime)

    user = relationship('User', back_populates='shopping_cart')
    items = relationship('Item', back_populates='shopping_cart')


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    shopping_cart_id = Column(Integer, ForeignKey('shopping_carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    reservation_identifier = Column(String)

    shopping_cart = relationship('ShoppingCart', back_populates='items')
    product = relationship('Product')
