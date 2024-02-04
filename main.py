from fastapi import FastAPI
from sqlalchemy import event

from api.controllers.items_controller import ItemsController
from api.database.configuration import engine, DBSession
from api.database.models import User, Base, Product
from api.database.seeder import seed_table

event.listen(User.__table__, 'after_create', seed_table)
event.listen(Product.__table__, 'after_create', seed_table)

app = FastAPI()

items_controller = ItemsController(DBSession())
app.include_router(items_controller.router)

@app.on_event("startup")
def configure():
    Base.metadata.create_all(bind=engine)











