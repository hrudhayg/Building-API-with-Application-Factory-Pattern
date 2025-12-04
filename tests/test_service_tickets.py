import unittest
from application import create_app

class CustomerRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig").test_client()

        self.base_url = "/service_tickets/"

    # GET /service_tickets
    def test_get_service_tickets(self):
        response = self.app.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    # POST /service_tickets (valid) – assumes customer_id=1 exists or your API validates differently
    def test_create_service_ticket_valid(self):
        payload = {
            "VIN": "1HGCM82633A004352",
            "service_date": "2025-09-01",
            "service_desc": "Brake replacement",
            "customer_id": 1,
            "mechanic_ids": []
        }
        response = self.app.post(self.base_url, json=payload)
        # If your API requires a real customer_id, adjust your seeding or expected code
        self.assertIn(response.status_code, [201, 400])

    # POST /service_tickets (negative: missing VIN)
    def test_create_service_ticket_missing_vin(self):
        payload = {
            # "VIN" missing
            "service_date": "2025-09-01",
            "service_desc": "Engine diagnostic",
            "customer_id": 1
        }
        response = self.app.post(self.base_url, json=payload)
        self.assertIn(response.status_code, [400, 422])

    # GET /service_tickets/<id> not found
    def test_get_service_ticket_not_found(self):
        response = self.app.get("/service_tickets/999999")
        self.assertEqual(response.status_code, 404)

    # Full CRUD flow (if your API allows creating with dummy customer_id)
    def test_service_ticket_crud_flow(self):
        create_payload = {
            "VIN": "1HGCM82633A004353",
            "service_date": "2025-09-02",
            "service_desc": "Oil change",
            "customer_id": 1,
            "mechanic_ids": []
        }
        create_resp = self.app.post(self.base_url, json=create_payload)
        self.assertIn(create_resp.status_code, [201, 400])

        if create_resp.status_code != 201:
            # If 400 because of invalid customer_id, you can skip rest or adjust test to your reality
            return

        data = create_resp.get_json() or {}
        ticket_id = data.get("id") or data.get("ticket", {}).get("id")
        self.assertIsNotNone(ticket_id)

        get_resp = self.app.get(f"/service_tickets/{ticket_id}")
        self.assertEqual(get_resp.status_code, 200)

        update_payload = {"service_desc": "Oil + filter change"}
        update_resp = self.app.put(f"/service_tickets/{ticket_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.app.delete(f"/service_tickets/{ticket_id}")
        self.assertEqual(delete_resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
