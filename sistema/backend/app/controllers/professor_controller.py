from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.professor import Professor
from app.models.usuario import Usuario
from app.utils.response import APIResponse

def get_professor(id):
    """Obtém os dados de um professor específico pelo ID."""

    
    try:
    
        prof = Professor.query.get(id)
        if prof:
            return APIResponse.success(data=prof.to_dict())

        return APIResponse.error("Professor não encontrado"
                                 , status_code=404)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados"
                                 ,status_code=500)

def create_professor():
    """
    Registra um novo professor a partir de um usuário existente.
    Espera dados JSON incluindo o ID do usuário e informações do professor.
    Retorna:
        201 em caso de sucesso ou erros 400/500 conforme a validação.
    """
    
    data = request.json
    user_id = data.get("id")
    
    try:
        if not user_id or not Usuario.query.get(user_id):
            return APIResponse.error(
                "Usuário não existe"
                ,status_code=400
            )
    
        prof = Professor(
            id=user_id
            ,salario=data.get("salario")
            ,graduacao=data.get("graduacao")
            ,descricao=data.get("descricao")
        )

        db.session.add(prof)
        db.session.commit()
        return APIResponse.success(
            "Professor criado com sucesso."
            ,status_code=201
        ) 
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error(
            "Já existe um professor para este usuário"
            ,status_code=400
        )
    
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados", status_code=500
        )
    
def update_professor(id):
    data = request.json

    try:
        prof = Professor.query.get(id)
        if not prof:
            return APIResponse.error(
                "Professor não encontrado"
                , status_code=404
            )
        
        prof.salario = data.get("salario", prof.salario)
        prof.graduacao = data.get("graduacao", prof.graduacao)
        prof.descricao = data.get("descricao", prof.descricao)

        db.session.commit()
        return APIResponse.success(
            "Professor atualizado com sucesso"
        )

    except IntegrityError:
        db.session.rollback()
        return APIResponse.error(
            "Dados violam restrições de integridade."
            ,status_code=400
        )
    
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados",
            status_code=500
        )

def delete_professor(id):
    try:
        prof = Professor.query.get(id)

        if not prof:
            return APIResponse.error(
                "Professor não encontrado"
                ,status_code=404
            )
        
        db.session.delete(prof)
        db.session.commit()
        return APIResponse.success("Professor removido com sucesso")
    
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
        )

def lista_professores():
    try:
        profs = Professor.query.all()
        data = [
            {
                **prof.to_dict()
                ,"nome_usuario":prof.usuario.nome + " " + prof.usuario.ultimo_nome
                ,
            } for prof in profs
        ]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)