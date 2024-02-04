from unittest import TestCase
from unittest.mock import patch, MagicMock

from api.jobs.reservation_jobs import ReserveItemJob, ReleaseReservedItemJob


class ReserveItemJobIntegrationTest(TestCase):
    def test_update_item(self):
        item_id = 1
        reservation_identifier = 'new_reservation_identifier'
        job = ReserveItemJob(item_id)

        mock_update_item = MagicMock(return_value=None)

        with patch.multiple(
            job,
            reserve_item=MagicMock(return_value=reservation_identifier),
            update_item=mock_update_item
        ) as mocks:
            job.handle()

            mock_update_item.assert_called_once_with(reservation_identifier)

        for mock in mocks:
            mock.assert_called_once()


class ReleaseReservedItemJobIntegrationTest(TestCase):
    def test_handle(self) -> None:
        item_id = 1
        job = ReleaseReservedItemJob(item_id)

        with patch.multiple(
            job,
            release_reserved_item=MagicMock(return_value=None),
            delete_item=MagicMock(return_value=None)
        ) as mocks:
            job.handle()

        for mock in mocks:
            mock.assert_called_once()
