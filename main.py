from fastapi import FastAPI

from api.controllers.items_controller import ItemsController
from api.database.configuration import Base, engine

app = FastAPI()

items_controller = ItemsController()

app.include_router(items_controller.router)

Base.metadata.create_all(engine)
