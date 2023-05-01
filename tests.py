import os

os.environ["DATABASE_URL"] = "postgresql:///cupcakes_test"

from unittest import TestCase

from app import app
from models import db, Cupcake

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "https://natashaskitchen.com/wp-content/uploads/2020/05/Vanilla-Cupcakes-3.jpg",
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg",
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """Test Cupcakes Listing"""
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(
                data,
                {
                    "cupcakes": [
                        {
                            "id": self.cupcake_id,
                            "flavor": "TestFlavor",
                            "size": "TestSize",
                            "rating": 5,
                            "image_url": "https://natashaskitchen.com/wp-content/uploads/2020/05/Vanilla-Cupcakes-3.jpg",
                        }
                    ]
                },
            )

    def test_get_cupcake(self):
        """Test Get Cupcake Detail"""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(
                data,
                {
                    "cupcake": {
                        "id": self.cupcake_id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image_url": "https://natashaskitchen.com/wp-content/uploads/2020/05/Vanilla-Cupcakes-3.jpg",
                    }
                },
            )

    def test_create_cupcake(self):
        """Test creation of new cupcake."""
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json["cupcake"]["id"]

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(
                resp.json,
                {
                    "cupcake": {
                        "id": cupcake_id,
                        "flavor": "TestFlavor2",
                        "size": "TestSize2",
                        "rating": 10,
                        "image_url": "http://test.com/cupcake2.jpg",
                    }
                },
            )

            self.assertEqual(Cupcake.query.count(), 2)

    def test_edit_cupcake(self):
        """Test editing a cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                {
                    "cupcake": {
                        "id": self.cupcake_id,
                        "flavor": "TestFlavor2",
                        "size": "TestSize2",
                        "rating": 10,
                        "image_url": "http://test.com/cupcake2.jpg",
                    }
                },
            )

    def test_edit_cupcake_404(self):
        """Test editing a cupcake with invalid id."""
        with app.test_client() as client:
            url = "/api/cupcakes/-1"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        """Test deleting a cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                {"deleted": self.cupcake_id},
            )

            self.assertEqual(Cupcake.query.count(), 0)

    def test_delete_cupcake_404(self):
        """Test deleting a cupcake with invalid id."""
        with app.test_client() as client:
            url = "/api/cupcakes/-1"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)


# Example of a curl request
# curl http://127.0.0.1:5001/api/cupcakes/1 \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{"flavor":"flavorType", "size":"sizeType", "rating":10, "image_url":""}'
