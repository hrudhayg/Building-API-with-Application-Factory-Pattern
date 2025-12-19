import unittest
from application import create_app

class CustomerRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig").test_client()

        self.base_url = "/inventory/"

    # GET /inventory
    def test_get_inventory(self):
        response = self.app.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    # POST /inventory (valid)
    def test_create_inventory_item_valid(self):
        payload = {
            "name": "Brake Pad",
            "price": 99.99
        }
        response = self.app.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201)

    # POST /inventory (negative: missing name)
    def test_create_inventory_item_missing_name(self):
        payload = {
            # "name" missing
            "price": 49.99
        }
        response = self.app.post(self.base_url, json=payload)
        self.assertIn(response.status_code, [400, 422])

    # GET /inventory/<id> not found
    def test_get_inventory_item_not_found(self):
        response = self.app.get("/inventory/999999/")
        self.assertEqual(response.status_code, 404)

    # Full CRUD flow
    def test_inventory_crud_flow(self):
        create_payload = {
            "name": "Oil Filter",
            "price": 25.00
        }
        create_resp = self.app.post(self.base_url, json=create_payload)
        self.assertEqual(create_resp.status_code, 201)

        data = create_resp.get_json() or {}
        part_id = data.get("id") or data.get("item", {}).get("id")
        self.assertIsNotNone(part_id)

        get_resp = self.app.get(f"/inventory/{part_id}")
        self.assertEqual(get_resp.status_code, 200)

        update_payload = {"price": 29.99}
        update_resp = self.app.put(f"/inventory/{part_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.app.delete(f"/inventory/{part_id}")
        self.assertEqual(delete_resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
