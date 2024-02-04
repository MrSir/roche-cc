from __future__ import annotations

from sqlalchemy.orm import Session

from api.database.configuration import DBSession
from api.database.models import Item
from api.jobs.base_jobs import Job


class BaseItemJob(Job):
    def __init__(self, item_id: int):
        self.item_id: int = item_id
        self.db_session: Session = DBSession()
        self._item: Item | None = None

    def queue(self) -> None:
        # TODO: add logic to create the appropriate queue locks so that jobs related to the same item or product do not
        #       get processed concurrently
        pass

    def before_start(self) -> None:
        # TODO: ensure that another job for the same item or product is not currently being processed. If there are any
        #       then leave this job back onto the queue for processing later
        pass

    @property
    def item(self) -> Item:
        if self._item is None:
            self._item = self.db_session.query(Item).filter(Item.id == self.item_id).first()

        return self._item


class ReserveItemJob(BaseItemJob):
    def reserve_item(self) -> str:
        if self.item.reservation_identifier is not None:
            # TODO: call external service with reservation identifier and update the quantity of the reservation
            return self.item.reservation_identifier

        # TODO: call external service with the specific product id from the item
        return 'new_reservation_identifier'

    def update_item(self, reservation_identifier: str) -> None:
        self.db_session.query(Item).filter(Item.id == self.item.id).update({
            Item.reservation_identifier: reservation_identifier
        })
        self.db_session.commit()

    def handle(self) -> None:
        reservation_identifier = self.reserve_item()

        self.update_item(reservation_identifier)


class ReleaseReservedItemJob(BaseItemJob):
    def release_reserved_item(self) -> None:
        # TODO: call external service to release the reservation by using the stored release identifier on the item
        pass

    def delete_item(self) -> None:
        self.db_session.delete(self.item)
        self.db_session.commit()

    def handle(self) -> None:
        self.release_reserved_item()
        self.delete_item()
