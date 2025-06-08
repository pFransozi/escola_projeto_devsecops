import os
import requests
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash
from app.utils.jwt import create_access_token, create_refresh_token
from flask import session

# --- Variáveis de Ambiente ---
COGNITO_DOMAIN        = os.getenv("AWS_COGNITO_DOMAIN")
COGNITO_REGION        = os.getenv("AWS_COGNITO_REGION", "us-east-2")
COGNITO_CLIENT_ID     = os.getenv("AWS_COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("AWS_COGNITO_CLIENT_SECRET")
REDIRECT_URI          = os.getenv("AWS_COGNITO_REDIRECT_URI")
if not all([COGNITO_DOMAIN, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET, REDIRECT_URI]):
    raise RuntimeError(
        "Configure AWS_COGNITO_DOMAIN, AWS_COGNITO_CLIENT_ID, "
        "AWS_COGNITO_CLIENT_SECRET e AWS_COGNITO_REDIRECT_URI no .env"
    )

# Endpoint de troca de código PKCE por tokens Cognito
TOKEN_URL = (
    f"https://{COGNITO_DOMAIN}.auth.{COGNITO_REGION}.amazoncognito.com"
    "/oauth2/token"
)


def exchange_code():
    """
    POST /api/auth/callback
    Fluxo PKCE + Cognito para administradores:
    - Recebe JSON { code, code_verifier }
    - Troca por tokens Cognito
    - Decodifica ID Token e extrai claims
    - Gera tokens locais JWT-HS256 com sub do Cognito
    - Retorna JSON com tokens e user info
    - Seta o refresh_token do Cognito em cookie HttpOnly
    """
    data = request.get_json(force=True)
    code = data.get("code")
    code_verifier = data.get("code_verifier")
    if not code or not code_verifier:
        return jsonify({"error": "Parâmetros inválidos"}), 400

    # Chamada ao Cognito
    payload = {
        "grant_type": "authorization_code",
        "client_id": COGNITO_CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier
    }
    auth = (COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)
    resp = requests.post(TOKEN_URL, data=payload, auth=auth)
    if resp.status_code != 200:
        return jsonify({"error": "Falha na troca de código", "details": resp.json()}), resp.status_code

    tokens = resp.json()
    id_token = tokens["id_token"]
    refresh_token = tokens["refresh_token"]
    expires_in = tokens.get("expires_in")

    # Decodifica ID Token
    from app.utils.jwt import decode_token
    claims = decode_token(id_token)

    # Monta informações do usuário a partir das claims
    user_info = {
        "id": claims.get("sub"),
        "nome": claims.get("given_name", ""),
        "email": claims.get("email", "")
    }

    # marca na sessão que é admin
    session.clear()
    session['user_id']  = user_info['id']
    session['is_admin'] = True

    # Gera tokens locais
    local_access = create_access_token(identity=user_info["id"])
    local_refresh = create_refresh_token(identity=user_info["id"])

    response = make_response(jsonify({
        "id_token": id_token,
        "access_token": local_access,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "user": user_info
    }), 200)
    # Cookie HttpOnly com refresh_token do Cognito
    secure_flag = os.getenv("FLASK_ENV") == "production"
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=secure_flag,
        samesite="Lax",
        max_age=30 * 24 * 3600
    )
    return response


def login_local():
    """
    POST /api/auth/login
    Autenticação local (professor, aluno etc.).
    """
    from app.models.usuario import Usuario

    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username e senha são obrigatórios"}), 400

    user = Usuario.query.filter_by(usuario=username).first()
    if not user or not check_password_hash(user.senha_hash, password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)

    session.clear()
    session['user_id']  = user.id
    session['is_admin'] = False

    return jsonify({
        "access_token": access,
        "refresh_token": refresh,
        "user": {"id": user.id, "nome": user.nome, "email": user.email}
    }), 200


def refresh_token():
    """
    POST /api/auth/refresh
    Renova access token local via JWT-Extended.
    """
    from flask_jwt_extended import jwt_required, get_jwt_identity

    @jwt_required()
    def _inner():
        user_id = get_jwt_identity()
        new_access = create_access_token(identity=user_id)
        return jsonify({"access_token": new_access}), 200
    return _inner()
