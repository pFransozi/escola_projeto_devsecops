from flask import Blueprint
from app.controllers.prova_controller import (
    lista_provas, get_prova,
    create_prova, update_prova, delete_prova
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

prova_bp = Blueprint("prova_bp", __name__)

prova_bp.route("", methods=["GET"], endpoint="lista_provas")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(lista_provas)
)
prova_bp.route("/<int:id>", methods=["GET"], endpoint="get_prova")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(get_prova)
)
prova_bp.route("", methods=["POST"], endpoint="create_prova")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(create_prova)
)
prova_bp.route("/<int:id>", methods=["PUT"], endpoint="update_prova")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(update_prova)
)
prova_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_prova")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(delete_prova)
)
