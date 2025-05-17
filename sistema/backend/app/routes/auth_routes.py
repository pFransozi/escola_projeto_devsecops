from flask import Blueprint
from app.controllers.auth_controller import login

auth_bp = Blueprint("auth_bp", __name__)

auth_bp.route("", methods=["POST"])(login)