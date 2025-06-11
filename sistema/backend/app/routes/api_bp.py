# Arquivo: sistema/backend/app/routes/api_bp.py
from flask import Blueprint

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

# Sub-blueprints
from app.routes.usuario_routes import user_bp
# from app.routes.auth_routes import auth_bp  # <--- REMOVA ESTA LINHA
from app.routes.dashboard_routes import dashboard_bp
from app.routes.professor_routes import professor_bp
from app.routes.estudante_routes import estudante_bp
# Garanta que o novo blueprint interno está sendo importado
from app.routes.internal_routes import internal_bp

# Registro dos sub-blueprints no api_bp
api_bp.register_blueprint(user_bp, url_prefix="/usuario")
# api_bp.register_blueprint(auth_bp, url_prefix="/auth") # <--- REMOVA ESTA LINHA
api_bp.register_blueprint(dashboard_bp, url_prefix="/dashboard")
api_bp.register_blueprint(professor_bp, url_prefix="/professor")
api_bp.register_blueprint(estudante_bp, url_prefix="/estudante")
# E também registrado
api_bp.register_blueprint(internal_bp, url_prefix="/internal")