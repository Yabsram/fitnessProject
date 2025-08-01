import unittest, sys, os

sys.path.append('../fitnessProject')
from app import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SECRET_KEY'] = 'test-secret'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    ###############
    #### tests ####
    ###############

    def register(self, username, email, password):
        return self.app.post('/register',
                            data=dict(username=username,
                                      email=email,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.register('valid_user', 'valid@example.com', 'ThisIsSupossedToBeSecret')
        self.assertEqual(response.status_code, 200)

    def test_invalid_username_registration(self):
        response = self.register('a', 'a@example.com', 'DoesNotMatter')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_email_registration(self):
        response = self.register('valid_user', 'invalid@example', 'SecurePassword')
        self.assertIn(b'Invalid email address.', response.data)

    def test_invalid_password_registration(self):
        response = self.register('valid_user', 'valid@example.com', 'No')
        self.assertIn(b'Field must be at least 8 characters long.', response.data)


if __name__ == "__main__":
    unittest.main()