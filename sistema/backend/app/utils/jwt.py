import os
import jwt
from jwt import PyJWKClient

# Chave para validar tokens locais (HS256)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY não configurada no .env")

# Configurações para validar tokens do Cognito (JWKS)
COGNITO_REGION = os.getenv("AWS_COGNITO_REGION", "us-east-2")
COGNITO_USER_POOL_ID = os.getenv("AWS_COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("AWS_COGNITO_CLIENT_ID")

if not all([COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID]):
    raise RuntimeError("Configure AWS_COGNITO_USER_POOL_ID e AWS_COGNITO_CLIENT_ID no .env")

# URL de JWKS baseada no User Pool
JWKS_URL = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    "/.well-known/jwks.json"
)
# Cliente para buscar as chaves públicas do Cognito, que será usado pelo middleware
jwk_client = PyJWKClient(JWKS_URL)