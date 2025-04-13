from flask import Blueprint
from app.controllers.auth_controller import login


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()