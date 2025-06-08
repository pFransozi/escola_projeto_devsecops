# app/utils/jwt.py

import os
import datetime
import jwt
from jwt import PyJWKClient

# --- Configurações de tokens locais (HS256) ---
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY não configurada no .env")

ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))          # 1 hora
REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", str(7 * 24 * 3600)))  # 7 dias

# --- Configurações do Cognito (JWKS) ---
COGNITO_REGION      = os.getenv("AWS_COGNITO_REGION", "us-east-2")
COGNITO_USER_POOL_ID = os.getenv("AWS_COGNITO_USER_POOL_ID")  # ID do User Pool
COGNITO_CLIENT_ID   = os.getenv("AWS_COGNITO_CLIENT_ID")      # Client ID usado como audience

if not all([COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID]):
    raise RuntimeError("Configure AWS_COGNITO_USER_POOL_ID e AWS_COGNITO_CLIENT_ID no .env")

# URL de JWKS baseada no User Pool
JWKS_URL = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    "/.well-known/jwks.json"
)
# Cliente para buscar e cachear as chaves públicas do Cognito
jwk_client = PyJWKClient(JWKS_URL)


def create_access_token(identity):
    """
    Cria um JWT de acesso local (HS256) para uso interno da API.
    """
    now = datetime.datetime.utcnow()
    payload = {
        "sub": identity,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=ACCESS_TOKEN_EXPIRES)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def create_refresh_token(identity):
    """
    Cria um JWT de refresh local (HS256) para uso interno da API.
    """
    now = datetime.datetime.utcnow()
    payload = {
        "sub": identity,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=REFRESH_TOKEN_EXPIRES)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token):
    """
    Verifica e decodifica um ID Token do Cognito (RS256) usando as chaves JWKS
    do User Pool. Valida assinatura e audiência (client_id).
    """
    # Seleciona a chave pública correta a partir do header 'kid'
    signing_key = jwk_client.get_signing_key_from_jwt(token).key
    # Decodifica, validando assinatura RS256 e a audiência
    payload = jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        audience=COGNITO_CLIENT_ID
    )
    return payload
