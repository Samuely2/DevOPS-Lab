# Arquivo: tests/test_app.py
import unittest
from app import app

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_login_success(self):
        response = self.client.post('/login', json={"username": "admin", "password": "admin"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_failure(self):
        response = self.client.post('/login', json={"username": "wrong", "password": "wrong"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Invalid credentials"})

    def test_create_categoria(self):
        login_response = self.client.post('/login', json={"username": "admin", "password": "admin"})
        token = login_response.json["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        data = {"nome": "Eletrônicos", "descricao": "Produtos eletrônicos diversos"}
        response = self.client.post('/categorias', json=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn("categoria", response.json)
        self.assertEqual(response.json["categoria"]["nome"], "Eletrônicos")

    def test_get_categorias(self):
        response = self.client.get('/categorias')
        self.assertEqual(response.status_code, 200)
        self.assertIn("categorias", response.json)

    def test_create_produto(self):
        login_response = self.client.post('/login', json={"username": "admin", "password": "admin"})
        token = login_response.json["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        categoria_data = {"nome": "Informática", "descricao": "Produtos de informática"}
        categoria_response = self.client.post('/categorias', json=categoria_data, headers=headers)
        categoria_id = categoria_response.json["categoria"]["id"]

        produto_data = {"nome": "Notebook", "preco": 2500.00, "categoria_id": categoria_id}
        response = self.client.post('/produtos', json=produto_data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn("produto", response.json)
        self.assertEqual(response.json["produto"]["nome"], "Notebook")

    def test_get_produtos(self):
        response = self.client.get('/produtos')
        self.assertEqual(response.status_code, 200)
        self.assertIn("produtos", response.json)

    def test_create_produto_invalid_categoria(self):
        login_response = self.client.post('/login', json={"username": "admin", "password": "admin"})
        token = login_response.json["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        produto_data = {"nome": "Celular", "preco": 1200.00, "categoria_id": "999"}
        response = self.client.post('/produtos', json=produto_data, headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Categoria inválida"})

if __name__ == '__main__':
    unittest.main()
