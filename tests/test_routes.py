"""API tests compatible with pytest and nosetests."""

import unittest

from service import create_app
from service.models import db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TALISMAN_FORCE_HTTPS = False


class AccountsTestCase(unittest.TestCase):
    """Accounts REST API tests."""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_create_account(self):
        response = self.client.post(
            "/api/accounts",
            json={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "address": "1 Main St",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Jane Doe")

    def test_list_accounts(self):
        self.client.post("/api/accounts", json={"name": "A", "email": "a@example.com"})
        self.client.post("/api/accounts", json={"name": "B", "email": "b@example.com"})
        response = self.client.get("/api/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_read_account(self):
        created = self.client.post(
            "/api/accounts", json={"name": "A", "email": "a@example.com"}
        ).json
        response = self.client.get(f"/api/accounts/{created['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["email"], "a@example.com")

    def test_update_account(self):
        created = self.client.post(
            "/api/accounts", json={"name": "A", "email": "a@example.com"}
        ).json
        response = self.client.put(
            f"/api/accounts/{created['id']}", json={"name": "Updated"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated")

    def test_delete_account(self):
        created = self.client.post(
            "/api/accounts", json={"name": "A", "email": "a@example.com"}
        ).json
        response = self.client.delete(f"/api/accounts/{created['id']}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            self.client.get(f"/api/accounts/{created['id']}").status_code, 404
        )

    def test_missing_required_fields(self):
        response = self.client.post("/api/accounts", json={"name": "Only Name"})
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email(self):
        payload = {"name": "A", "email": "a@example.com"}
        self.assertEqual(self.client.post("/api/accounts", json=payload).status_code, 201)
        self.assertEqual(self.client.post("/api/accounts", json=payload).status_code, 409)

    def test_security_and_cors_headers(self):
        response = self.client.get("/")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        cors_response = self.client.get("/api/accounts")
        self.assertEqual(cors_response.headers.get("Access-Control-Allow-Origin"), "*")


if __name__ == "__main__":
    unittest.main()
