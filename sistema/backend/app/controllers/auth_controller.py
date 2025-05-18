# auth_controller.py

from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    """
    Endpoint de login descontinuado.
    A autenticação agora é feita via AWS Cognito Hosted UI.
    """
    return jsonify({
        "success": False,
        "message": "Endpoint de login desativado. Use o fluxo do AWS Cognito."
    }), 400
