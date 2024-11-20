from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Configuração do Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Banco de dados em memória
produtos_db = {}
categorias_db = {}

@app.route('/')
def index():
    return send_from_directory('static', 'swagger-ui.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin":
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    return jsonify(error="Invalid credentials"), 401

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1313)

