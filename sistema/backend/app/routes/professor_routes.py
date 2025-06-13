from flask import Blueprint
from app.controllers.professor_controller import (
    get_professor, create_professor, update_professor, delete_professor, lista_professores
)
from app.utils.decorators import role_required
from app.models.usuario import UsuarioTipoEnum

professor_bp = Blueprint("professor_bp", __name__)

professor_bp.route('', methods=['GET', 'OPTIONS'], endpoint='lista_professores')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(lista_professores)
)
professor_bp.route('/<int:id>', methods=['GET'], endpoint='get_professor')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(get_professor)
)
professor_bp.route('', methods=['POST'], endpoint='create_professor')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(create_professor)
)
professor_bp.route('/<int:id>', methods=['PUT'], endpoint='update_professor')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(update_professor)
)
professor_bp.route('/<int:id>', methods=['DELETE'], endpoint='delete_professor')(
    role_required(roles=[UsuarioTipoEnum.Secretario])(delete_professor)
)