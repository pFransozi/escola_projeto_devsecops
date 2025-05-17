from flask import Blueprint
from app.controllers.usuario_controller import (
    lista_usuarios,
    get_usuario,
    cadastrar_usuario,
    update_usuario,
    delete_usuario
)

user_bp = Blueprint("user_bp", __name__)

user_bp.route("",             methods=["GET"])(lista_usuarios)
user_bp.route("/<int:id>",    methods=["GET"])(get_usuario)
user_bp.route("",             methods=["POST"])(cadastrar_usuario)
user_bp.route("/<int:id>",    methods=["PUT"])(update_usuario)
user_bp.route("/<int:id>",    methods=["DELETE"])(delete_usuario)
