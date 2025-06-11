# Arquivo: sistema/backend/app/utils/decorators.py
# VERSÃO FINAL E CORRIGIDA

from functools import wraps
from flask import g, jsonify
from app.models.usuario import UsuarioTipoEnum

def admin_required(fn):
    """Verifica se o usuário é um administrador logado via Cognito."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not g.get('cognito_claims'):
            return jsonify({"error": "Acesso negado. Esta rota é apenas para administradores autenticados via Cognito."}), 403
        
        user_groups = g.cognito_claims.get('cognito:groups', [])
        if 'Admins' not in user_groups:
            return jsonify({"error": "Acesso negado: Requer privilégios de administrador no grupo 'Admins'."}), 403
        
        return fn(*args, **kwargs)

def role_required(roles=[]):
    """
    Verifica se o usuário logado (local ou Cognito) possui um dos papéis necessários.
    `roles` é uma lista de membros do UsuarioTipoEnum.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not g.get('user'):
                return jsonify({"error": "Acesso não autorizado: Requer autenticação."}), 401
            
            user_type = g.user.get('tipo')

            if user_type == 'cognito_admin':
                return fn(*args, **kwargs)
            
            # Compara o tipo do usuário (string) com os valores do enum na lista
            if roles and user_type not in [r.value for r in roles]:
                role_values = [str(r.value) for r in roles]
                return jsonify({"error": f"Acesso negado. Requer um dos seguintes papéis: {', '.join(role_values)}"}), 403
            
            return fn(*args, **kwargs)
        
        # --- A CORREÇÃO CRUCIAL ---
        # A função 'decorator' DEVE retornar a função 'wrapper'.
        return wrapper
        
    return decorator