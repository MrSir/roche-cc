from fastapi import FastAPI

from api.controllers.items_controller import ItemsController
from api.database.configuration import Base, engine
from api.database.models import User, Product

app = FastAPI()

items_controller = ItemsController()

app.include_router(items_controller.router)

Base.metadata.create_all(engine)

# Seed some data
Product(id=1, name='Computer', is_active=True, price=1500.00)
Product(id=2, name='Monitor', is_active=True, price=500.00)

User(id=1, email='mitkomtoshev@gmail.com', hashed_password='Test1234ngjkdgndfgj', is_active=True)
