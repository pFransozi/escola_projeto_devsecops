import os
import jwt
from jwt import PyJWKClient
from flask import request, g, jsonify

from app.models.usuario import Usuario  # importa seu modelo

# Carrega as variáveis do Cognito do ambiente
COGNITO_REGION        = os.getenv('AWS_COGNITO_REGION')
COGNITO_USER_POOL_ID  = os.getenv('AWS_COGNITO_USER_POOL_ID')
COGNITO_APP_CLIENT_ID = os.getenv('AWS_COGNITO_CLIENT_ID')

# Endpoint JWKS para obter as chaves públicas do Cognito
jwks_url = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"
    f"{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
)
jwks_client = PyJWKClient(jwks_url)

def autenticacao():
    # Permite preflight de CORS
    if request.method == "OPTIONS":
        return '', 200

    # Captura header Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Não autorizado: token ausente"}), 401

    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({"error": "Não autorizado: formato de token inválido"}), 401

    token = parts[1]

    # Busca a chave pública correta pelo kid
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except Exception:
        return jsonify({"error": "Token JWT inválido"}), 401

    # Decodifica e valida o token
    try:
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=COGNITO_APP_CLIENT_ID,
            issuer=(
                f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"
                f"{COGNITO_USER_POOL_ID}"
            )
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Não autorizado: token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Não autorizado: token inválido"}), 401

    # Sincroniza usuário Cognito ↔ banco local
    sub   = payload.get("sub")
    email = payload.get("email")

    usuario = Usuario.get_by_cognito_sub_or_email(sub, email)
    if not usuario:
        return jsonify({
            "error": "Usuário não cadastrado no sistema. Contate o administrador."
        }), 403

    # Anexa o objeto Usuario do SQLAlchemy ao contexto
    g.user = usuario

    # Se retornar None, continua a execução normalmente
    return None
