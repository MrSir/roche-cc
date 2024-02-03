from __future__ import annotations

from functools import cached_property

from api.database.configuration import DBSession
from api.database.models import Item
from api.jobs.base_jobs import Job


class BaseItemJob(Job):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.db_session = DBSession
        self._item: Item | None = None

    @cached_property
    def item(self) -> Item:
        if self._item is None:
            self._item = self.db_session.query(Item).filter(Item.id == self.item_id).first()

        return self._item


class ReserveItemJob(BaseItemJob):
    def handle(self) -> None:
        reservation_identifier = self.reserve_item(self.item)

        self.update_item(self.item, reservation_identifier)

    def reserve_item(self, item: Item) -> str:
        if item.reservation_identifier is not None:
            # call external service with reservation identifier and update the quantity of the reservation
            pass
        else:
            # call external service with the specific product id from the item
            pass

        return 'reservation_identifier_1234'

    def update_item(self, item: Item, reservation_identifier: str) -> None:
        self.db_session.query(Item).filter(Item.id == item.id).update({
            Item.reservation_identifier: reservation_identifier
        })
        self.db_session.commit()
        self.db_session.refresh(item)


class ReleaseReservedItemJob(BaseItemJob):
    def handle(self) -> None:
        self.release_reserved_item(self.item)
        self.delete_item(self.item)

    def release_reserved_item(self, item: Item) -> None:
        # call external service to release the reservation by using the stored release identifier on the item
        pass

    def delete_item(self, item: Item) -> None:
        self.db_session.delete(item)
        self.db_session.commit()
