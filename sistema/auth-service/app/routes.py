from flask import Blueprint, request, jsonify
from . import services
from .utils.jwt import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/callback", methods=['POST'])
def handle_callback():
    data = request.get_json()
    try:
        tokens = services.exchange_code_for_tokens(data.get("code"), data.get("code_verifier"))
        return jsonify(tokens), 200
    except Exception as e:
        return jsonify({"error": "Falha na troca de código com o Cognito", "details": str(e)}), 500

@auth_bp.route("/login", methods=['POST'])
def handle_local_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username e senha são obrigatórios"}), 400

    try:
        user_data = services.authenticate_local_user(username, password)
        access_token = create_access_token(identity=user_data['id'])
        return jsonify({
            "access_token": access_token,
            "user": user_data
        }), 200
    except Exception as e:
        return jsonify({"error": "Credenciais inválidas"}), 401