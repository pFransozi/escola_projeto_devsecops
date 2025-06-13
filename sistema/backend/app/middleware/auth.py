import os
import jwt
from jwt import PyJWKClient
from flask import request, g, jsonify
# A importação deve ser absoluta a partir da raiz 'app'
from app.utils.jwt import JWT_SECRET_KEY, jwk_client, COGNITO_CLIENT_ID, COGNITO_REGION, COGNITO_USER_POOL_ID

def autenticacao():
    """
    Middleware de autenticação que intercepta todas as requisições ao backend.
    Verifica se a rota solicitada requer token de autorização e, caso positivo,
    valida o token JWT (Cognito ou local) presente no cabeçalho Authorization.
    Retorna uma resposta de erro JSON e código HTTP 401/403 se a autenticação falhar.
    """
    # Permite requisições pré-voo de CORS
    if request.method == "OPTIONS":
        return None
    
    # --- A CORREÇÃO CRUCIAL ---
    # Define quais rotas são públicas e não precisam de um token de autorização.
    # A rota interna de validação DEVE estar aqui.
    public_paths = ['/api/internal/validate-user']
    if request.path in public_paths:
        return None
    # --- FIM DA CORREÇÃO ---

    # Para todas as outras rotas, exige um token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Não autorizado: token ausente ou mal formatado"}), 401
    
    token = auth_header.split(" ")[1]
    
    # Tenta validar como um token do Cognito (RS256)
    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID,
            issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}",
        )
        g.user = {'id': payload.get('sub'), 'tipo': 'cognito_admin'}
        g.cognito_claims = payload
        return None
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        pass # Se não for um token do Cognito, ignora o erro e tenta o próximo método

    # Tenta validar como um token Local (HS256)
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        from app.models.usuario import Usuario
        # payload['sub'] vem do token e deve ser uma string
        user = Usuario.query.get(payload['sub'])
        if user:
            g.user = user.to_dict()
        else:
            raise jwt.exceptions.InvalidTokenError("Usuário do token não encontrado no banco de dados.")
        return None
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Não autorizado: token expirado"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"Não autorizado: token inválido. {e}"}), 401

    return jsonify({"error": "Não foi possível validar o token por nenhum método."}), 401