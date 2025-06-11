# Arquivo: sistema/backend/app/routes/estudante_routes.py
from flask import Blueprint
from app.controllers.estudante_controller import (
    get_estudante, create_estudante, update_estudante, delete_estudante, lista_estudantes
)
# --- Imports atualizados ---
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

estudante_bp = Blueprint("estudante_bp", __name__)

# --- Rotas corrigidas com decorador e endpoint ---
estudante_bp.route("", methods=["GET", "OPTIONS"], endpoint='lista_estudantes')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(lista_estudantes)
)
estudante_bp.route("/<int:id>", methods=["GET"], endpoint='get_estudante')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(get_estudante)
)
estudante_bp.route("", methods=["POST"], endpoint='create_estudante')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(create_estudante)
)
estudante_bp.route("/<int:id>", methods=["PUT"], endpoint='update_estudante')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(update_estudante)
)
estudante_bp.route("/<int:id>", methods=["DELETE"], endpoint='delete_estudante')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(delete_estudante)
)