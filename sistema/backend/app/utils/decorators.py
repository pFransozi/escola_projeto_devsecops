from functools import wraps
from flask import session, jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # se não estiver logado ou não for admin, bloqueia
        if not session.get('user_id') or not session.get('is_admin'):
            return jsonify({"error": "Acesso negado"}), 403
        return fn(*args, **kwargs)
    return wrapper
