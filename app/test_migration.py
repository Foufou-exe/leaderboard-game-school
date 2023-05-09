import unittest
from app import app

# TEST MIGRATION
class TestMigrationApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.app.post("/register", data=data)
        self.assertEqual(response.status_code, 302)

        # test that user can log in after registering
        response = self.app.post(
            "/login", data={"username": "testuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, 302)

        # test that user can reset password after registering
        response = self.app.post(
            "/reset_password",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)

        # test that user can log in with new password
        response = self.app.post(
            "/login", data={"username": "testuser", "password": "newpassword123"}
        )
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
