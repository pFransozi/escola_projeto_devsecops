from flask import Blueprint
from app.controllers.professor_controller import (
    get_professor,
    create_professor,
    update_professor,
    delete_professor,
    lista_professores
)

professor_bp = Blueprint("professor_bp", __name__)

professor_bp.route("/<int:id>", methods=["GET"])(get_professor)
professor_bp.route("", methods=["GET", "OPTIONS"])(lista_professores)
professor_bp.route("", methods=["POST"])(create_professor)
professor_bp.route("/<int:id>", methods=["PUT"])(update_professor)
professor_bp.route("/<int:id>", methods=["DELETE"])(delete_professor)

