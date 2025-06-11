# Arquivo: sistema/backend/tests/test_routes.py

import json

def test_dashboard_unauthorized(test_client):
    """
    GIVEN um cliente de teste
    WHEN uma requisição GET é feita para /api/dashboard SEM um token
    THEN a resposta deve ser 401 Unauthorized
    """
    response = test_client.get('/api/dashboard')
    assert response.status_code == 401
    assert "token ausente ou mal formatado" in response.get_json()["error"]

def test_dashboard_authorized(test_client, db_session, auth_headers):
    """
    GIVEN um cliente de teste
    WHEN uma requisição GET é feita para /api/dashboard COM um token válido
    THEN a resposta deve ser 200 OK e conter os dados do dashboard
    """
    # Gera um token para um usuário do tipo 'aluno'
    headers = auth_headers(user_type='aluno')
    
    response = test_client.get('/api/dashboard', headers=headers)
    data = response.get_json()

    assert response.status_code == 200
    assert "users" in data
    assert "professores" in data

def test_user_list_forbidden(test_client, db_session, auth_headers):
    """
    GIVEN um usuário com papel de 'aluno'
    WHEN uma requisição GET é feita para /api/usuario (que requer papel 'secretario')
    THEN a resposta deve ser 403 Forbidden
    """
    # Gera um token para um usuário do tipo 'aluno'
    headers = auth_headers(user_type='aluno')

    response = test_client.get('/api/usuario', headers=headers)
    data = response.get_json()

    assert response.status_code == 403
    assert "Acesso negado" in data["error"]

def test_user_list_allowed(test_client, db_session, auth_headers):
    """
    GIVEN um usuário com papel de 'secretario'
    WHEN uma requisição GET é feita para /api/usuario
    THEN a resposta deve ser 200 OK
    """
    # Gera um token para um usuário do tipo 'secretario'
    headers = auth_headers(user_type='secretario')
    
    response = test_client.get('/api/usuario', headers=headers)
    assert response.status_code == 200