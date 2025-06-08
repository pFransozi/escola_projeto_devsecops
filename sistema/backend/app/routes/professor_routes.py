from flask import Blueprint
from app.controllers.professor_controller import (
    get_professor,
    create_professor,
    update_professor,
    delete_professor,
    lista_professores
)

from app.utils.decorators import admin_required


professor_bp = Blueprint("professor_bp", __name__)

professor_bp.route('', methods=['GET', 'OPTIONS'])(admin_required(lista_professores))
professor_bp.route('/<int:id>', methods=['GET'])(admin_required(get_professor))
professor_bp.route('', methods=['POST'])(admin_required(create_professor))
professor_bp.route('/<int:id>', methods=['PUT'])(admin_required(update_professor))
professor_bp.route('/<int:id>', methods=['DELETE'])(admin_required(delete_professor))

