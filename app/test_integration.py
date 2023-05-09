import unittest
from unittest.mock import patch
from app import app, User

# TEST INTEGRATION
class TestIntegrationLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # Test d'integration pour la route de login
    @patch.object(User, "find_by_username")
    @patch("app.check_password_hash")
    def test_login_post(self, mock_hash, mock_find):
        mock_user = User("1", "testuser", "test@example.com", "newpassword123")
        mock_find.return_value = mock_user
        mock_hash.return_value = True
        response = self.app.post(
            "/login", data=dict(username="username", password="password")
        )
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
