from flask import request, jsonify, g
from werkzeug.security import generate_password_hash
from app.models.user import User, UserTipoEnum
from app.extensions import db


def cadastrar_usuario():

    if not hasattr(g, "user") or g.user.tipo != UserTipoEnum.Admin:
        return (
            jsonify(
                {
                    "error": "Acesso negado. Apenas administradores podem cadastrar usuários"
                }
            ),
            403,
        )

    data = request.get_json()
    required = [
        "nome",
        "usuario",
        "senha",
        "cpf",
        "data_nascimento",
        "sexo",
        "endereco",
        "tipo",
    ]

    try:

        if not all(field in data for field in required):
            return jsonify({"error": "Dados incompletos"}), 400

        if User.query.filter_by(usuario=data["login"]).first():
            return jsonify({"error": "Login já cadastrado"}), 400

        novo_usuario = User(
            nome=data["nome"],
            ultimo_nome=data["ultimo_nome"],
            usuario=data["login"],
            senha=generate_password_hash(data["senha"]),
            email=data.get("email"),
            data_nascimento=data["data_nascimento"],
            sexo=data["sexo"],
            cpf=data["cpf"],
            endereco=data["endereco"],
            tipo=data["tipo"],
            id_user_insert=g.user.id,
        )

        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso!"}), 201
    
    except Exception as e:

        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
