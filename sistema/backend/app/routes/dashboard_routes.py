from flask import Blueprint, request, make_response
from app.controllers.dashboard_controller import dashboard_data

dashboard_bp = Blueprint("dashboard_db", __name__)

@dashboard_bp.route("", methods=["GET"])
def get_dashboard():
    return dashboard_data()