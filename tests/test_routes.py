"""TDD test suite for the Customer Accounts REST service."""

import unittest
from datetime import date

from service import create_app
from service.models import db


class TestConfig:
    """Isolated test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TALISMAN_FORCE_HTTPS = False


class AccountsTestCase(unittest.TestCase):
    """Accounts API tests."""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app = None

    @staticmethod
    def payload(**overrides):
        data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "address": "1 Main St",
            "phone_number": "555-0100",
            "date_joined": "2025-01-15",
        }
        data.update(overrides)
        return data

    def create_account(self, **overrides):
        response = self.client.post("/accounts", json=self.payload(**overrides))
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"name": "Account REST API Service", "version": "1.0"})

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_create_account(self):
        account = self.create_account()
        self.assertEqual(account["name"], "Jane Doe")
        self.assertEqual(account["phone_number"], "555-0100")
        self.assertEqual(account["date_joined"], "2025-01-15")
        self.assertTrue(self.client.get(response_location(self.client, account["id"])).status_code in (200, 404))

    def test_create_missing_required_field(self):
        response = self.client.post("/accounts", json={"name": "Only Name"})
        self.assertEqual(response.status_code, 400)

    def test_create_bad_media_type(self):
        response = self.client.post(
            "/accounts",
            data='{"name":"Jane","email":"jane@example.com","address":"Main"}',
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 415)

    def test_duplicate_email(self):
        self.create_account()
        response = self.client.post("/accounts", json=self.payload())
        self.assertEqual(response.status_code, 409)

    def test_list_accounts(self):
        self.create_account(email="a@example.com")
        self.create_account(name="John Doe", email="b@example.com")
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_read_account(self):
        account = self.create_account()
        response = self.client.get(f"/accounts/{account['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "jane@example.com")

    def test_read_missing_account(self):
        response = self.client.get("/accounts/999")
        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        account = self.create_account()
        response = self.client.put(
            f"/accounts/{account['id']}",
            json={"name": "Updated Name", "address": "2 Main St"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated Name")
        self.assertEqual(response.get_json()["address"], "2 Main St")

    def test_update_missing_account(self):
        response = self.client.put("/accounts/999", json={"name": "Updated"})
        self.assertEqual(response.status_code, 404)

    def test_update_bad_media_type(self):
        account = self.create_account()
        response = self.client.put(
            f"/accounts/{account['id']}",
            data="{}",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 415)

    def test_update_duplicate_email(self):
        self.create_account(email="one@example.com")
        second = self.create_account(name="Second", email="two@example.com")
        response = self.client.put(
            f"/accounts/{second['id']}",
            json={"email": "one@example.com"},
        )
        self.assertEqual(response.status_code, 409)

    def test_delete_account(self):
        account = self.create_account()
        response = self.client.delete(f"/accounts/{account['id']}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.get(f"/accounts/{account['id']}").status_code, 404)

    def test_delete_missing_account_is_idempotent(self):
        response = self.client.delete("/accounts/999")
        self.assertEqual(response.status_code, 204)

    def test_api_aliases(self):
        response = self.client.post("/api/accounts", json=self.payload(email="api@example.com"))
        self.assertEqual(response.status_code, 201)
        account_id = response.get_json()["id"]
        self.assertEqual(self.client.get(f"/api/accounts/{account_id}").status_code, 200)
        self.assertEqual(self.client.get("/api/accounts").status_code, 200)

    def test_security_headers_and_cors(self):
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(
            response.headers.get("Content-Security-Policy"),
            "default-src 'self'; object-src 'none'",
        )
        self.assertEqual(
            response.headers.get("Referrer-Policy"),
            "strict-origin-when-cross-origin",
        )
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")

    def test_model_helpers(self):
        from service.models import Account, DataValidationError

        account = Account()
        with self.assertRaises(DataValidationError):
            account.deserialize(None)
        with self.assertRaises(DataValidationError):
            account.deserialize({"name": "Only Name"})
        with self.assertRaises(DataValidationError):
            account.deserialize(self.payload(date_joined="not-a-date"))
        account.deserialize(self.payload())
        self.assertEqual(account.date_joined, date(2025, 1, 15))
        self.assertIsNone(Account.find_by_email("does-not-exist@example.com"))


def response_location(client, account_id):
    """Return the canonical URL used by a created Account."""
    return f"/accounts/{account_id}"


if __name__ == "__main__":
    unittest.main()
