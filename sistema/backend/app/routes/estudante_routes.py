from flask import Blueprint
from app.controllers.estudante_controller import (
    get_estudante,
    create_estudante,
    update_estudante,
    delete_estudante,
    lista_estudantes,
)

from app.utils.decorators import admin_required


estudante_bp = Blueprint("estudante_bp", __name__)

estudante_bp.route("", methods=["GET", "OPTIONS"])(admin_required(lista_estudantes))
estudante_bp.route("/<int:id>", methods=["GET"])(admin_required(get_estudante))
estudante_bp.route("", methods=["POST"])(admin_required(create_estudante))
estudante_bp.route("/<int:id>", methods=["PUT"])(admin_required(update_estudante))
estudante_bp.route("/<int:id>", methods=["DELETE"])(admin_required(delete_estudante))
