import unittest
from application import create_app

class CustomerRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig").test_client()

        self.base_url = "/mechanics/"

    # GET /mechanics
    def test_get_mechanics(self):
        response = self.app.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    # POST /mechanics (valid)
    def test_create_mechanic_valid(self):
        payload = {
            "name": "Brock",
            "email": "brock@example.com",
            "phone": "555-444-3333",
            "salary": 4500
        }
        response = self.app.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201)

    # POST /mechanics (negative: missing required field)
    def test_create_mechanic_missing_field(self):
        payload = {
            "name": "NoSalary",
            "email": "nosalary@example.com",
            "phone": "555-111-1111"
            # salary missing
        }
        response = self.app.post(self.base_url, json=payload)
        self.assertIn(response.status_code, [400, 422])

    # GET /mechanics/<id> not found
    def test_get_mechanic_not_found(self):
        response = self.app.get("/mechanics/999999/")
        self.assertEqual(response.status_code, 404)

    # Full CRUD flow for mechanic
    def test_mechanic_crud_flow(self):
        create_payload = {
            "name": "CrudMechanic",
            "email": "crud_mech@example.com",
            "phone": "555-999-8888",
            "salary": 5000
        }
        create_resp = self.app.post(self.base_url, json=create_payload)
        self.assertEqual(create_resp.status_code, 201)

        data = create_resp.get_json() or {}
        mechanic_id = data.get("id") or data.get("mechanic", {}).get("id")
        self.assertIsNotNone(mechanic_id)

        get_resp = self.app.get(f"/mechanics/{mechanic_id}")
        self.assertEqual(get_resp.status_code, 200)

        update_payload = {"salary": 5500}
        update_resp = self.app.put(f"/mechanics/{mechanic_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.app.delete(f"/mechanics/{mechanic_id}")
        self.assertEqual(delete_resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
