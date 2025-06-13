from flask import Blueprint

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

# Sub-blueprints
from app.routes.usuario_routes import user_bp

from app.routes.dashboard_routes import dashboard_bp
from app.routes.professor_routes import professor_bp
from app.routes.estudante_routes import estudante_bp
from app.routes.atividade_routes import atividade_bp
from app.routes.disciplina_routes import disciplina_bp
from app.routes.turma_routes import turma_bp
from app.routes.noticia_routes import noticia_bp
from app.routes.atividade_escolar_routes import atividade_escolar_bp
from app.routes.aula_routes import aula_bp
from app.routes.prova_routes import prova_bp
from app.routes.internal_routes import internal_bp

# Registro dos sub-blueprints no api_bp
api_bp.register_blueprint(user_bp, url_prefix="/usuario")
api_bp.register_blueprint(dashboard_bp, url_prefix="/dashboard")
api_bp.register_blueprint(professor_bp, url_prefix="/professor")
api_bp.register_blueprint(estudante_bp, url_prefix="/estudante")
api_bp.register_blueprint(atividade_bp, url_prefix="/atividade")
api_bp.register_blueprint(disciplina_bp, url_prefix="/disciplina")
api_bp.register_blueprint(turma_bp, url_prefix="/turma")
api_bp.register_blueprint(noticia_bp, url_prefix="/noticia")
api_bp.register_blueprint(atividade_escolar_bp, url_prefix="/atividade_escolar")
api_bp.register_blueprint(aula_bp, url_prefix="/aula")
api_bp.register_blueprint(prova_bp, url_prefix="/prova")


api_bp.register_blueprint(internal_bp, url_prefix="/internal")
