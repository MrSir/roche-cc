class ReserveJob:
    def __init__(self, item_id: int):
        self.item_id = item_id

    def queue(self) -> None:
        """Put's the current task onto the configured queue for processing asynchronously"""

    def handle(self) -> None:
        pass
        # call external service
        # update reservation_identifier on the item
