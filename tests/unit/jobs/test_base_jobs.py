from unittest import TestCase

from api.jobs.base_jobs import Job


class JobUnitTest(TestCase):
    def test_init(self) -> None:
        job = Job()

        self.assertTrue(hasattr(job, 'queue'))
        self.assertTrue(hasattr(job, 'before_start'))
