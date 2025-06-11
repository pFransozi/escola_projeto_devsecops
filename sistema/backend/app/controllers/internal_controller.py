from flask import request, jsonify
from app.models.usuario import Usuario
from werkzeug.security import check_password_hash

def validate_local_user_credentials():
    """
    Recebe username/password e valida contra o banco de dados.
    Esta função só deve ser chamada por outros serviços internos.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição está vazio ou não é JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username e password são obrigatórios"}), 400

    user = Usuario.query.filter_by(usuario=username).first()

    if not user:
        print(f"--- FALHA: Usuário '{username}' não encontrado no banco de dados. ---", flush=True)
        return jsonify({"error": "Credenciais inválidas"}), 401
    
    password_is_valid = check_password_hash(user.senha, password)

    if password_is_valid:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401