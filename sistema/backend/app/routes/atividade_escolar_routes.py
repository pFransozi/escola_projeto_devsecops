from flask import Blueprint
from app.controllers.atividade_escolar_controller import (
    lista_atividades_escolares, get_atividade_escolar,
    create_atividade_escolar, update_atividade_escolar, delete_atividade_escolar
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

atividade_escolar_bp = Blueprint("atividade_escolar_bp", __name__)

atividade_escolar_bp.route("", methods=["GET"], endpoint="lista_atividades_escolares")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(lista_atividades_escolares)
)
atividade_escolar_bp.route("/<int:id>", methods=["GET"], endpoint="get_atividade_escolar")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(get_atividade_escolar)
)
atividade_escolar_bp.route("", methods=["POST"], endpoint="create_atividade_escolar")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(create_atividade_escolar)
)
atividade_escolar_bp.route("/<int:id>", methods=["PUT"], endpoint="update_atividade_escolar")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(update_atividade_escolar)
)
atividade_escolar_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_atividade_escolar")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(delete_atividade_escolar)
)
