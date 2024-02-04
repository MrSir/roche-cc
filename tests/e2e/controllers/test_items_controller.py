from unittest import TestCase

from fastapi.testclient import TestClient

from api.database.models import User
from main import app


class ItemsControllerE2ETest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_index_success(self) -> None:
        User(id=1, email='mitkomtoshev@gmail.com', hashed_password='Test1234ngjkdgndfgj', is_active=True)

        response = self.client.get('/items')

        print(response.json())
