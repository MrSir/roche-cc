from fastapi import FastAPI

from api.controllers.items_controller import ItemsController
from api.database.configuration import SessionLocal

app = FastAPI()

items_controller = ItemsController(SessionLocal)

app.include_router(items_controller.router)
