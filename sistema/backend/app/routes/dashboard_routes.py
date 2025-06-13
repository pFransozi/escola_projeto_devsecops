from flask import Blueprint
from app.controllers.dashboard_controller import dashboard_data
from app.utils.decorators import role_required

# Cria o Blueprint normalmente
dashboard_bp = Blueprint("dashboard_db", __name__)

@dashboard_bp.route("", methods=["GET"])
@role_required(roles=[])
def get_dashboard():
    """
    Esta é a função de visualização (view function) para a rota do dashboard.
    Ela é protegida pelo decorador e chama a lógica do controller.
    """
    # A lógica para buscar os dados continua no controller, o que é uma boa prática.
    return dashboard_data()