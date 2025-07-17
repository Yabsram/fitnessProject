import unittest, sys

sys.path.append('../fitnessProject')
from app import app 

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SECRET_KEY'] = 'test-secret'
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_workouts_page(self):
        response = self.app.get('/workouts', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_recipes_page(self):
        response = self.app.get('/recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page_and_logout(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()