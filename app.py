from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para todas as rotas
CORS(app)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

### Swagger UI ###
SWAGGER_URL = '/swagger'
API_DOC_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_DOC_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return jsonify(message="API is running")

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items=["item1", "item2", "item3"])

@app.route('/item/<string:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    items = {"1": "item1", "2": "item2", "3": "item3"}
    item = items.get(item_id)
    if not item:
        return jsonify(error="Item not found"), 404
    return jsonify(item=item)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Simulando validação de login
    if username == "test" and password == "test":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify(error="Invalid credentials"), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello, {current_user}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1313)
