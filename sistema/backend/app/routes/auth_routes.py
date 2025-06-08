# app/routes/auth_routes.py
from flask import Blueprint
from app.controllers.auth_controller import login_local, exchange_code, refresh_token

auth_bp = Blueprint('auth_bp', __name__)

# POST /api/auth/login
@auth_bp.route('/login', methods=['POST'])
def route_login():
    return login_local()

# POST /api/auth/callback
@auth_bp.route('/callback', methods=['POST'])
def route_callback():
    return exchange_code()

# POST /api/auth/refresh
@auth_bp.route('/refresh', methods=['POST'])
def route_refresh():
    return refresh_token()
