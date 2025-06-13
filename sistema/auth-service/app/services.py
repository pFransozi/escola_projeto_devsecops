import requests
from flask import current_app
from .config import Config

def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    """
    Troca um código de autorização por tokens de acesso/atualização no Cognito.
    Parâmetros:
        code (str): Código de autorização recebido do Cognito após login do usuário.
        code_verifier (str): Verificador do código (PKCE) utilizado na autenticação.
    Retorna:
        dict: Um dicionário com tokens (access token, refresh token, id token) retornados pelo Cognito.
    """
    payload = {
        "grant_type": "authorization_code",
        "client_id": Config.COGNITO_CLIENT_ID,
        "code": code,
        "redirect_uri": Config.REDIRECT_URI,
        "code_verifier": code_verifier,
    }
    
    auth = (Config.COGNITO_CLIENT_ID, Config.COGNITO_CLIENT_SECRET)

    response = requests.post(Config.TOKEN_URL, data=payload, auth=auth)
    response.raise_for_status()  # Lança uma exceção para status 4xx/5xx
    
    return response.json()

def authenticate_local_user(username, password):
    """
    Autentica um usuário local (não Cognito) chamando o endpoint interno do backend.
    Parâmetros:
        username (str): Nome de usuário (login) do usuário.
        password (str): Senha em texto plano para autenticação.
    Retorna:
        dict: Dados do usuário (por exemplo, id, tipo, etc.) se as credenciais forem válidas.
    Lança:
        Exception: Se as credenciais forem inválidas ou ocorrer erro na comunicação com o backend.
    """
    backend_url = current_app.config["INTERNAL_BACKEND_URL"]
    validation_endpoint = f"{backend_url}/api/internal/validate-user"
    
    payload = {"username": username, "password": password}

    # 'verify=False' é necessário porque o backend está usando um certificado
    # autoassinado. Em produção, isso deveria ser um certificado válido.
    response = requests.post(validation_endpoint, json=payload, verify=False)

    # Se a resposta do backend não for 200 OK, levanta um erro
    response.raise_for_status()
    
    # Retorna os dados do usuário (ex: id, tipo, etc.)
    return response.json()