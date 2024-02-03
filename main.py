from fastapi import FastAPI

from api.controllers.items_controller import ItemsController


app = FastAPI()

items_controller = ItemsController()

app.include_router(items_controller.router)
