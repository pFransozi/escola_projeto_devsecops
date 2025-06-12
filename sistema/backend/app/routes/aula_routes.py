from flask import Blueprint
from app.controllers.aula_controller import (
    lista_aulas, get_aula,
    create_aula, update_aula, delete_aula
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

aula_bp = Blueprint("aula_bp", __name__)

aula_bp.route("", methods=["GET"], endpoint="lista_aulas")(
    role_required(roles=[UsuarioTipoEnum.Professor])(lista_aulas)
)
aula_bp.route("/<int:id>", methods=["GET"], endpoint="get_aula")(
    role_required(roles=[UsuarioTipoEnum.Professor])(get_aula)
)
aula_bp.route("", methods=["POST"], endpoint="create_aula")(
    role_required(roles=[UsuarioTipoEnum.Professor])(create_aula)
)
aula_bp.route("/<int:id>", methods=["PUT"], endpoint="update_aula")(
    role_required(roles=[UsuarioTipoEnum.Professor])(update_aula)
)
aula_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_aula")(
    role_required(roles=[UsuarioTipoEnum.Professor])(delete_aula)
)
