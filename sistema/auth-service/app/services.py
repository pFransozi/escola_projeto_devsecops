import requests
from flask import current_app
from .config import Config

def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
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
    Chama o endpoint interno do backend para validar as credenciais.
    Retorna os dados do usuário se a chamada for bem-sucedida.
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