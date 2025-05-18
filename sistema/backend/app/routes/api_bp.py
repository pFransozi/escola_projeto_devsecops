from flask import Blueprint

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

# Sub-blueprints
from app.routes.usuario_routes import user_bp
from app.routes.auth_routes import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.professor_routes import professor_bp
from app.routes.estudante_routes import estudante_bp

# Registro dos sub-blueprints no api_bp
api_bp.register_blueprint(user_bp, url_prefix="/usuario")
api_bp.register_blueprint(auth_bp, url_prefix="/login")
api_bp.register_blueprint(dashboard_bp, url_prefix="/dashboard")
api_bp.register_blueprint(professor_bp, url_prefix="/professor")
api_bp.register_blueprint(estudante_bp, url_prefix="/estudante")
