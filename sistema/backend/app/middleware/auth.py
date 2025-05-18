import os
import jwt
from jwt import PyJWKClient
from flask import request, g, jsonify

# Carrega as variáveis do Cognito
COGNITO_REGION       = os.getenv('AWS_COGNITO_REGION')
COGNITO_USER_POOL_ID = os.getenv('AWS_COGNITO_USER_POOL_ID')
COGNITO_APP_CLIENT_ID = os.getenv('AWS_COGNITO_CLIENT_ID')

# URL para obter as chaves públicas do Cognito
jwks_url = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"
    f"{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
)
jwks_client = PyJWKClient(jwks_url)

def autenticacao():
    # Permite requisições CORS preflight
    if request.method == "OPTIONS":
        return '', 200

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Não autorizado: token ausente"}), 401

    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({"error": "Não autorizado: formato de token inválido"}), 401

    token = parts[1]

    # Obtém a chave pública correta pelo kid
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except Exception:
        return jsonify({"error": "Token JWT inválido"}), 401

    # Valida e decodifica o token
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

    # Grava os dados do usuário no contexto Flask
    g.user = {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "payload": payload
    }
    # Se retornar None, prossegue; caso contrário, aborta
    return None
