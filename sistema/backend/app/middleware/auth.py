import os
import jwt
from jwt import PyJWKClient
from flask import request, g, jsonify

# Carrega as variáveis do Cognito do ambiente
COGNITO_REGION        = os.getenv("AWS_COGNITO_REGION")
COGNITO_USER_POOL_ID  = os.getenv("AWS_COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("AWS_COGNITO_CLIENT_ID")

# Endpoint JWKS para obter as chaves públicas do Cognito
jwks_url = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"
    f"{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
)
jwks_client = PyJWKClient(jwks_url)


def autenticacao():
    # 1) Permite preflight de CORS
    if request.method == "OPTIONS":
        return "", 200

    # 2) Ignora as rotas de auth (login, callback, refresh)
    if request.path.startswith("/api/auth"):
        return None

    # 3) Autenticação via sessão (login session-based)
    from flask import session
    if session.get('user_id'):
        # Se houver sessão de usuário, continua sem exigir JWT header
        return None

    # 4) Autenticação via JWT Cognito em header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Não autorizado: token ausente"}), 401

    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({"error": "Não autorizado: formato de token inválido"}), 401

    token = parts[1]

    # 5) Obtém a chave pública correta a partir do JWT
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except Exception:
        return jsonify({"error": "Token JWT inválido"}), 401

    # 6) Decodifica e valida o token
    try:
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=COGNITO_APP_CLIENT_ID,
            issuer=(
                f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"
                f"{COGNITO_USER_POOL_ID}"
            ),
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Não autorizado: token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Não autorizado: token inválido"}), 401

    # 7) Armazena as claims do Cognito no contexto
    g.cognito_claims = payload
    return None
    # Permite preflight de CORS
    if request.method == "OPTIONS":
        return "", 200

    # Ignora as rotas de auth (login, callback, refresh)
    if request.path.startswith("/api/auth"):
        return None

    # Captura o header Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Não autorizado: token ausente"}), 401

    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({"error": "Não autorizado: formato de token inválido"}), 401

    token = parts[1]

    # Obtém a chave pública correta a partir do JWT
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
            ),
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Não autorizado: token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Não autorizado: token inválido"}), 401

    # Armazena as claims do Cognito no contexto, SEM verificar no BD local
    g.cognito_claims = payload

    # Continua a execução normalmente
    return None
