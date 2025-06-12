from flask import Blueprint
from app.controllers.disciplina_controller import (
    lista_disciplinas,
    get_disciplina,
    create_disciplina,
    update_disciplina,
    delete_disciplina,
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

disciplina_bp = Blueprint("disciplina_bp", __name__)

disciplina_bp.route("", methods=["GET"], endpoint="lista_disciplinas")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(
        lista_disciplinas
    )
)
disciplina_bp.route("/<int:id>", methods=["GET"], endpoint="get_disciplina")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(
        get_disciplina
    )
)
disciplina_bp.route("", methods=["POST"], endpoint="create_disciplina")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(
        create_disciplina
    )
)
disciplina_bp.route("/<int:id>", methods=["PUT"], endpoint="update_disciplina")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(
        update_disciplina
    )
)
disciplina_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_disciplina")(
    role_required(roles=[UsuarioTipoEnum.Secretario, UsuarioTipoEnum.Professor])(
        delete_disciplina
    )
)
