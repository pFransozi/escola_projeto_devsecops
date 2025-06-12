from flask import Blueprint
from app.controllers.noticia_controller import (
    lista_noticias, get_noticia,
    create_noticia, update_noticia, delete_noticia
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

noticia_bp = Blueprint("noticia_bp", __name__)

noticia_bp.route("", methods=["GET"], endpoint="lista_noticias")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(lista_noticias)
)
noticia_bp.route("/<int:id>", methods=["GET"], endpoint="get_noticia")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(get_noticia)
)
noticia_bp.route("", methods=["POST"], endpoint="create_noticia")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(create_noticia)
)
noticia_bp.route("/<int:id>", methods=["PUT"], endpoint="update_noticia")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(update_noticia)
)
noticia_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_noticia")(
    role_required(roles=[UsuarioTipoEnum.Secretario])(delete_noticia)
)
