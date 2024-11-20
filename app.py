from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Configuração do Flask e dependências
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Configuração do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Dados iniciais de categorias e produtos
categorias_db = {
    "1": {"id": "1", "nome": "Eletrônicos", "descricao": "Produtos eletrônicos como smartphones e laptops."},
    "2": {"id": "2", "nome": "Livros", "descricao": "Diversos tipos de livros, desde literatura até ciência."},
    "3": {"id": "3", "nome": "Roupas", "descricao": "Vestuário para homens e mulheres."},
    "4": {"id": "4", "nome": "Alimentos", "descricao": "Alimentos frescos e congelados."}
}

produtos_db = {
    "1": {"id": "1", "nome": "Smartphone XYZ", "preco": 999.99, "categoria_id": "1"},
    "2": {"id": "2", "nome": "Laptop ABC", "preco": 1499.99, "categoria_id": "1"},
    "3": {"id": "3", "nome": "Camiseta Casual", "preco": 29.99, "categoria_id": "3"},
    "4": {"id": "4", "nome": "Calça Jeans", "preco": 79.99, "categoria_id": "3"},
    "5": {"id": "5", "nome": "Livro de Ficção", "preco": 19.90, "categoria_id": "2"},
    "6": {"id": "6", "nome": "Livro Técnico", "preco": 59.90, "categoria_id": "2"},
    "7": {"id": "7", "nome": "Feijão Preto", "preco": 3.99, "categoria_id": "4"},
    "8": {"id": "8", "nome": "Arroz Integral", "preco": 4.99, "categoria_id": "4"}
}

# Rota inicial
@app.route('/')
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API!",
        "categorias": list(categorias_db.values()),
        "produtos": list(produtos_db.values())
    }), 200

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin":
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    return jsonify(error="Invalid credentials"), 401

# Rotas para categorias
@app.route('/categorias', methods=['POST'])
@jwt_required()
def create_categoria():
    data = request.json
    categoria_id = str(len(categorias_db) + 1)
    nome = data.get("nome")
    descricao = data.get("descricao")

    if not nome or not descricao:
        return jsonify(error="Nome e descrição são obrigatórios"), 400

    categorias_db[categoria_id] = {"id": categoria_id, "nome": nome, "descricao": descricao}
    return jsonify(message="Categoria criada", categoria=categorias_db[categoria_id]), 201

@app.route('/categorias', methods=['GET'])
def get_categorias():
    return jsonify(categorias=list(categorias_db.values())), 200

# Rotas para produtos
@app.route('/produtos', methods=['POST'])
@jwt_required()
def create_produto():
    data = request.json
    produto_id = str(len(produtos_db) + 1)
    nome = data.get("nome")
    preco = data.get("preco")
    categoria_id = data.get("categoria_id")

    if not all([nome, preco, categoria_id]):
        return jsonify(error="Todos os campos são obrigatórios"), 400
    if categoria_id not in categorias_db:
        return jsonify(error="Categoria inválida"), 404

    produtos_db[produto_id] = {"id": produto_id, "nome": nome, "preco": preco, "categoria_id": categoria_id}
    return jsonify(message="Produto criado", produto=produtos_db[produto_id]), 201

@app.route('/produtos', methods=['GET'])
def get_produtos():
    return jsonify(produtos=list(produtos_db.values())), 200

# Inicialização da aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1313)
