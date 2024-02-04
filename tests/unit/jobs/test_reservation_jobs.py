from unittest import TestCase
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from api.database.models import Item
from api.jobs.base_jobs import Job
from api.jobs.reservation_jobs import BaseItemJob, ReserveItemJob, ReleaseReservedItemJob


class BaseItemJobUnitTest(TestCase):
    def test_init(self) -> None:
        item_id = 1
        job = BaseItemJob(item_id)

        self.assertIsInstance(job, Job)
        self.assertEqual(item_id, job.item_id)
        self.assertIsInstance(job.db_session, Session)
        self.assertIsNone(job._item)

        self.assertTrue(hasattr(job, 'queue'))
        self.assertTrue(hasattr(job, 'before_start'))

    def test_item_returns_preset(self) -> None:
        item_id = 1
        job = BaseItemJob(item_id)

        item = Item(id=item_id)
        job._item = item

        self.assertEqual(item, job.item)

    def test_item_resolves_from_id(self) -> None:
        item_id = 1
        job = BaseItemJob(item_id)

        item = Item(id=item_id)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_db_session)
        mock_db_session.filter = MagicMock(return_value=mock_db_session)
        mock_db_session.first = MagicMock(return_value=item)

        job.db_session = mock_db_session

        self.assertEqual(item, job.item)


class ReserveItemJobUnitTest(TestCase):
    def test_init(self) -> None:
        item_id = 1
        job = ReserveItemJob(item_id)

        self.assertIsInstance(job, BaseItemJob)

    def test_reserve_item_updates_existing_reservation(self) -> None:
        item_id = 1
        reservation_identifier = 'existing_reservation_identifier'
        job = ReserveItemJob(item_id)
        job._item = Item(id=item_id, reservation_identifier=reservation_identifier)

        self.assertEqual(reservation_identifier, job.reserve_item())

    def test_reserve_item_creates_new_reservation(self) -> None:
        item_id = 1
        reservation_identifier = 'new_reservation_identifier'
        job = ReserveItemJob(item_id)
        job._item = Item(id=item_id)

        self.assertEqual(reservation_identifier, job.reserve_item())

    def test_update_item(self) -> None:
        item_id = 1
        reservation_identifier = 'new_reservation_identifier'
        job = ReserveItemJob(item_id)
        job._item = Item(id=item_id)

        mock_db_session = MagicMock()
        mock_db_session.query = MagicMock(return_value=mock_db_session)
        mock_db_session.filter = MagicMock(return_value=mock_db_session)
        mock_db_session.update = MagicMock(return_value=None)
        mock_db_session.commit = MagicMock(return_value=None)

        job.db_session = mock_db_session

        job.update_item(reservation_identifier)

        mock_db_session.query.assert_called_once_with(Item)
        mock_db_session.filter.assert_called_once()
        mock_db_session.update.assert_called_once_with(
            {Item.reservation_identifier: reservation_identifier}
        )
        mock_db_session.commit.assert_called_once()


class ReleaseReservedItemJobUnitTest(TestCase):
    def test_init(self) -> None:
        item_id = 1
        job = ReleaseReservedItemJob(item_id)

        self.assertIsInstance(job, BaseItemJob)

    def test_delete_item(self) -> None:
        item_id = 1
        item = Item(id=item_id)
        job = ReleaseReservedItemJob(item_id)
        job._item = item

        mock_db_session = MagicMock()
        mock_db_session.delete = MagicMock(return_value=None)
        mock_db_session.commit = MagicMock(return_value=None)

        job.db_session = mock_db_session

        job.delete_item()

        mock_db_session.delete.assert_called_once_with(item)
        mock_db_session.commit.assert_called_once()
