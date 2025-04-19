from flask import Blueprint, request, make_response
from app.controllers.dashboard_controller import dashboard_data

dashboard_bp = Blueprint("dashboard_db", __name__)

@dashboard_bp.route("/dashboard", methods=["GET", "OPTIONS"])
def get_dashboard():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "X-User-Id, Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return response, 200

    return dashboard_data()