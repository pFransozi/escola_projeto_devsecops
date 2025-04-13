from flask import request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User


def login():
    data = request.get_json()
    print("JSON recebido no backend:", data)

    login = data.get("usuario")
    senha = data.get("senha")

    if not login or not senha:
        return (
            jsonify({"Sucesso": False, "message": "Usuário e senha obrigatórios."}),
            400,
        )

    user = User.query.filter_by(usuario=login).first()
    if user and user.check_password(senha):
        return (jsonify({"success": True, "user": user.to_dict()}), 200)

    return (jsonify({"success": False, "message": "Credenciais Inválidas"}), 401)
