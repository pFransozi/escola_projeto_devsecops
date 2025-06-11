# Arquivo: sistema/backend/tests/conftest.py
# VERSÃO FINAL E CORRIGIDA

import pytest
from app import create_app, db
from faker import Faker
import datetime
import jwt
from app.models.usuario import Usuario, UsuarioTipoEnum

@pytest.fixture(scope='function')
def test_app():
    """Cria uma instância da aplicação com config de teste para cada teste."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')  # CORREÇÃO: O escopo deve ser 'function'
def test_client(test_app):
    """Cria um cliente de teste para fazer requisições HTTP."""
    return test_app.test_client()

# --- NOVA FIXTURE ADICIONADA ---
@pytest.fixture(scope='function')
def db_session(test_app):
    """Fornece o objeto 'db' para interagir com o banco de dados."""
    yield db
# --- FIM DA NOVA FIXTURE ---

def _create_test_token(identity, secret_key):
    """Helper interna para criar um token JWT apenas para testes."""
    payload = {
        "sub": str(identity), "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

@pytest.fixture(scope="function")
def auth_headers(test_app, db_session):
    """Gera cabeçalhos de autenticação para um usuário de teste."""
    from app.models.usuario import Usuario, UsuarioTipoEnum

    def _get_headers(user_type='aluno'): # Recebe a string 'aluno', 'secretario', etc.
        
        # --- INÍCIO DA CORREÇÃO ---
        # Converte a string recebida (ex: 'aluno') para o membro do Enum correspondente.
        user_type_enum = UsuarioTipoEnum(user_type)
        # --- FIM DA CORREÇÃO ---

        fake = Faker('pt_BR')
        cpf_limpo = ''.join(filter(str.isdigit, fake.cpf()))
        
        # Agora, usamos o 'user_type_enum' que é um objeto Enum
        user = Usuario(
            nome="Test", ultimo_nome="User", usuario=f"test_{user_type_enum.value}",
            senha="password", email=f"test_{user_type_enum.value}@test.com",
            data_nascimento="2000-01-01", sexo="M", cpf=cpf_limpo,
            endereco="Rua Teste", tipo=user_type_enum # Passa o Enum para o modelo
        )
        db_session.session.add(user)
        db_session.session.commit()

        secret = test_app.config["JWT_SECRET_KEY"]
        token = _create_test_token(user.id, secret)
        
        return {"Authorization": f"Bearer {token}"}

    return _get_headers

@pytest.fixture(scope='function')
def new_user_data():
    """Fornece um dicionário com dados de um novo usuário."""
    fake = Faker('pt_BR')
    cpf_limpo = ''.join(filter(str.isdigit, fake.cpf()))
    return {
        "nome": fake.first_name(), "ultimo_nome": fake.last_name(),
        "usuario": fake.user_name(), "senha": "password123",
        "email": fake.email(), "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=60),
        "sexo": "M", "cpf": cpf_limpo, "endereco": fake.address(), "tipo": "aluno"
    }