from flask import Blueprint
from app.controllers.usuario_controller import cadastrar_usuario

user_db = Blueprint("user_bp", __name__)

@user_db.route("/usuarios", methods=["POST"])
def cadastrar_usuario_route():
    return cadastrar_usuario()