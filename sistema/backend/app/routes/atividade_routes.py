from flask import Blueprint
from app.controllers.atividade_controller import (
    lista_atividades, get_atividade,
    create_atividade, update_atividade, delete_atividade
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

atividade_bp = Blueprint("atividade_bp", __name__)

atividade_bp.route("", methods=["GET"], endpoint="lista_atividades")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(lista_atividades)
)
atividade_bp.route("/<int:id>", methods=["GET"], endpoint="get_atividade")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(get_atividade)
)
atividade_bp.route("", methods=["POST"], endpoint="create_atividade")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(create_atividade)
)
atividade_bp.route("/<int:id>", methods=["PUT"], endpoint="update_atividade")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(update_atividade)
)
atividade_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_atividade")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(delete_atividade)
)
