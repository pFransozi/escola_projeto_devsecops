from flask import Blueprint
from app.controllers.usuario_controller import (
    lista_usuarios,
    get_usuario,
    cadastrar_usuario,
    update_usuario,
    delete_usuario
)
from app.utils.decorators import admin_required


user_bp = Blueprint("user_bp", __name__)

user_bp.route('', methods=['GET'])(admin_required(lista_usuarios))
user_bp.route('/<int:id>', methods=['GET'])(admin_required(get_usuario))
user_bp.route('', methods=['POST'])(admin_required(cadastrar_usuario))
user_bp.route('/<int:id>', methods=['PUT'])(admin_required(update_usuario))
user_bp.route('/<int:id>', methods=['DELETE'])(admin_required(delete_usuario))
