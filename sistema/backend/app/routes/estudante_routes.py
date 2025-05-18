from flask import Blueprint
from app.controllers.estudante_controller import (
    get_estudante
    ,create_estudante
    ,update_estudante
    ,delete_estudante
    ,lista_estudantes
)

estudante_bp = Blueprint(
    "estudante_bp"
    ,__name__
)

estudante_bp.route("/<int:id>", methods=["GET"])(get_estudante)
estudante_bp.route("", methods=["GET", "OPTION"])(lista_estudantes)
estudante_bp.route("",           methods=["POST"])(create_estudante)
estudante_bp.route("/<int:id>", methods=["PUT"])(update_estudante)
estudante_bp.route("/<int:id>", methods=["DELETE"])(delete_estudante)
