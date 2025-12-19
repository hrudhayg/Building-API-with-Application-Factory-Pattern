import unittest
from application import create_app

class CustomerRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig").test_client()

        self.base_url = "/customers/"

    # GET /customers
    def test_get_customers_list(self):
        response = self.app.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    # POST /customers (valid)
    def test_create_customer_valid(self):
        payload = {
            "name": "Ash",
            "email": "ash_test@example.com",
            "phone": "555-111-2222",
            "password": "Secret123!"
        }
        response = self.app.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201)

    # POST /customers (negative: missing required field)
    def test_create_customer_invalid_missing_field(self):
        payload = {
            "name": "NoPhone",
            "email": "no_phone@example.com",
            # "phone" is missing on purpose
            "password": "Secret123!"
        }
        response = self.app.post(self.base_url, json=payload)
        # Adjust if your API uses 422 or something else
        self.assertIn(response.status_code, [400, 422])

    # POST /customers/login (positive)
    def test_customer_login_success(self):
        # First ensure a customer exists
        payload = {
            "name": "LoginUser",
            "email": "login_user@example.com",
            "phone": "555-999-0000",
            "password": "LoginPass123"
        }
        self.app.post(self.base_url, json=payload)

        login_payload = {
            "email": "login_user@example.com",
            "password": "LoginPass123"
        }
        response = self.app.post("/customers/login/", json=login_payload)
        self.assertEqual(response.status_code, 200)

    # POST /customers/login (negative: wrong password)
    def test_customer_login_wrong_password(self):
        login_payload = {
            "email": "login_user@example.com",
            "password": "WrongPassword"
        }
        response = self.app.post("/customers/login/", json=login_payload)
        self.assertIn(response.status_code, [400, 401])

    # GET /customers/<id> (negative: not found)
    def test_get_customer_not_found(self):
        response = self.app.get("/customers/999999/")
        self.assertEqual(response.status_code, 404)

    # Full flow: create → get → update → delete
    def test_customer_crud_flow(self):
        # Create
        create_payload = {
            "name": "CrudUser",
            "email": "crud@example.com",
            "phone": "555-333-2222",
            "password": "CrudPass123"
        }
        create_resp = self.app.post(self.base_url, json=create_payload)
        self.assertEqual(create_resp.status_code, 201)

        created_data = create_resp.get_json() or {}
        customer_id = created_data.get("id")
        # If your API returns {"customer": { "id": ... }}, adjust this line
        if customer_id is None and "customer" in created_data:
            customer_id = created_data["customer"]["id"]

        self.assertIsNotNone(customer_id)

        # Get
        get_resp = self.app.get(f"/customers/{customer_id}")
        self.assertEqual(get_resp.status_code, 200)

        # Update
        update_payload = {
            "phone": "555-000-0000"
        }
        update_resp = self.app.put(f"/customers/{customer_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200)

        # Delete
        delete_resp = self.app.delete(f"/customers/{customer_id}")
        self.assertEqual(delete_resp.status_code, 200)

        # Confirm deleted (should be 404 now)
        get_again_resp = self.app.get(f"/customers/{customer_id}")
        self.assertEqual(get_again_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
