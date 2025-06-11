# auth-service/app/utils/jwt.py - Versão Simplificada
import datetime
import jwt
from flask import current_app

def create_access_token(identity):
    """Cria um JWT de acesso local (HS256)."""
    secret = current_app.config["JWT_SECRET_KEY"]
    payload = {
        "sub": str(identity),
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
    }
    return jwt.encode(payload, secret, algorithm="HS256")