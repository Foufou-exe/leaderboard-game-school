import unittest
from app import User
from werkzeug.security import generate_password_hash

# TEST UNIT
class TestUnitaireUser(unittest.TestCase):
    def test_check_password(self):
        password_hash = generate_password_hash("password123")
        user = User(1, "test", "test@test.com", password_hash)
        self.assertTrue(user.check_password("password123"))

    def test_user_model(self):
        user = User("1", "testuser", "test@example.com", "password123")
        self.assertEqual(user.get_id(), "1")
        self.assertTrue(user.is_authenticated())
        self.assertTrue(user.is_active())


if __name__ == "__main__":
    unittest.main()
