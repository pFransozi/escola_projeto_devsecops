from flask import Blueprint
from app.controllers.user_controller import cadastrar_usuario

user_db = Blueprint("user_bp", __name__)

@user_db.route("/usuarios", methods=["POST"])
def registrar_usuario():
    return cadastrar_usuario()