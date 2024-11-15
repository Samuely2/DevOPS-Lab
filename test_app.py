import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em Werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Criação do cliente de teste
        cls.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})

    def test_login_success(self):
        response = self.client.post('/login', json={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_failure(self):
        response = self.client.post('/login', json={"username": "wrong", "password": "wrong"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Invalid credentials"})

    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"items": ["item1", "item2", "item3"]})

    def test_get_item_by_id_success(self):
        response = self.client.get('/item/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"item": "item1"})

    def test_get_item_by_id_not_found(self):
        response = self.client.get('/item/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Item not found"})

    def test_protected_with_token(self):
        # Obter um token de login
        login_response = self.client.post('/login', json={"username": "test", "password": "test"})
        token = login_response.json.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}

        # Usar o token para acessar a rota protegida
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, test", response.json["message"])

    def test_protected_without_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
