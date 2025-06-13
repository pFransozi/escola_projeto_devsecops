from flask import Blueprint
from app.controllers.usuario_controller import (
    lista_usuarios, get_usuario, cadastrar_usuario, update_usuario, delete_usuario
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

user_bp = Blueprint("user_bp", __name__)

user_bp.route('', methods=['GET'], endpoint='lista_usuarios')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(lista_usuarios)
)
user_bp.route('/<int:id>', methods=['GET'], endpoint='get_usuario')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(get_usuario)
)
user_bp.route('', methods=['POST'], endpoint='cadastrar_usuario')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(cadastrar_usuario)
)
user_bp.route('/<int:id>', methods=['PUT'], endpoint='update_usuario')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(update_usuario)
)
user_bp.route('/<int:id>', methods=['DELETE'], endpoint='delete_usuario')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(delete_usuario)
)