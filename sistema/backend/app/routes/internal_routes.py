# sistema/backend/app/routes/internal_routes.py
from flask import Blueprint
from app.controllers.internal_controller import validate_local_user_credentials

# Usamos um prefixo 'internal' para deixar claro que são rotas internas
internal_bp = Blueprint("internal_bp", __name__)

internal_bp.route("/validate-user", methods=['POST'])(validate_local_user_credentials)