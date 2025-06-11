# Arquivo: sistema/backend/tests/test_models.py
import pytest
from app.models.usuario import Usuario, UsuarioTipoEnum
from app.models.professor import Professor
from app.models.estudante import Estudante
from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

def test_create_user(test_app, new_user_data):
    """
    GIVEN um modelo Usuario
    WHEN um novo usuário é criado com dados válidos
    THEN verifique se os campos foram definidos corretamente e a senha está hasheada
    """
    hashed_password = generate_password_hash(new_user_data['senha'])
    user = Usuario(
        nome=new_user_data['nome'],
        ultimo_nome=new_user_data['ultimo_nome'],
        usuario=new_user_data['usuario'],
        senha=hashed_password,
        email=new_user_data['email'],
        data_nascimento=new_user_data['data_nascimento'],
        sexo=new_user_data['sexo'],
        cpf=new_user_data['cpf'],
        endereco=new_user_data['endereco'],
        tipo=UsuarioTipoEnum(new_user_data['tipo'])
    )

    assert user.nome == new_user_data['nome']
    assert user.usuario == new_user_data['usuario']
    assert user.tipo == UsuarioTipoEnum.Aluno
    assert user.senha != new_user_data['senha']

def test_password_hashing(test_app, new_user_data):
    """
    GIVEN um modelo Usuario
    WHEN a senha é verificada com check_password_hash
    THEN verifique se senhas corretas e incorretas são tratadas adequadamente
    """
    hashed_password = generate_password_hash(new_user_data['senha'])
    user = Usuario(senha=hashed_password)

    assert user.check_password(new_user_data['senha']) is True
    assert user.check_password("wrongpassword") is False

def test_duplicate_username_raises_error(test_app, new_user_data):
    """
    GIVEN um banco de dados com um usuário existente
    WHEN um novo usuário é criado com o mesmo username
    THEN uma IntegrityError deve ser levantada pelo banco de dados
    """
    user1 = Usuario(**new_user_data)
    db.session.add(user1)
    db.session.commit()

    user2_data = new_user_data.copy()
    user2_data['cpf'] = '00011122233'
    user2 = Usuario(**user2_data)
    
    db.session.add(user2)
    with pytest.raises(IntegrityError):
        db.session.commit()

# --- NOVOS TESTES PARA PROFESSOR E ESTUDANTE ---

def test_create_professor(test_app, new_user_data):
    """
    GIVEN um usuário existente do tipo professor
    WHEN um novo registro de Professor é criado e associado a ele
    THEN verifique se o relacionamento e os campos estão corretos
    """
    new_user_data['tipo'] = UsuarioTipoEnum.Professor
    user = Usuario(**new_user_data)
    db.session.add(user)
    db.session.commit()

    professor_data = {
        "id": user.id,
        "salario": 7500.50,
        "graduacao": "Doutorado em Ciência da Computação"
    }
    professor = Professor(**professor_data)
    db.session.add(professor)
    db.session.commit()

    assert professor.id == user.id
    assert professor.salario == 7500.50
    assert professor.usuario.nome == new_user_data['nome']


def test_create_estudante(test_app, new_user_data):
    """
    GIVEN um usuário existente do tipo aluno
    WHEN um novo registro de Estudante é criado e associado a ele
    THEN verifique se o relacionamento e os campos estão corretos
    """
    new_user_data['tipo'] = UsuarioTipoEnum.Aluno
    user = Usuario(**new_user_data)
    db.session.add(user)
    db.session.commit()

    estudante_data = {
        "id": user.id,
        "responsavel_1": "Maria Silva",
        "fone_resp_1": "41999998888",
        "responsavel_2": "João Silva",
        "fone_resp_2": "41988889999",
        "comentarios": "Aluno dedicado."
    }
    estudante = Estudante(**estudante_data)
    db.session.add(estudante)
    db.session.commit()

    assert estudante.id == user.id
    assert estudante.responsavel_1 == "Maria Silva"
    assert estudante.usuario.usuario == new_user_data['usuario']