from flask import Blueprint
from app.controllers.turma_controller import (
    lista_turmas, get_turma,
    create_turma, update_turma, delete_turma
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

turma_bp = Blueprint("turma_bp", __name__)

turma_bp.route("", methods=["GET"], endpoint="lista_turmas")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(lista_turmas)
)
turma_bp.route("/<int:id>", methods=["GET"], endpoint="get_turma")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(get_turma)
)
turma_bp.route("", methods=["POST"], endpoint="create_turma")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(create_turma)
)
turma_bp.route("/<int:id>", methods=["PUT"], endpoint="update_turma")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(update_turma)
)
turma_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_turma")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(delete_turma)
)
