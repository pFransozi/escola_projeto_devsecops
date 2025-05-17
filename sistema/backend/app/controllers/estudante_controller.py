from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.estudante import Estudante
from app.models.usuario import Usuario
from app.utils.response import APIResponse
from datetime import datetime, timezone

def get_estudante(id):
    try:
        estudante= Estudante.query.get(id)
        if estudante:
            return APIResponse.success(
                data=estudante.to_dict()
                )
        
        return APIResponse.error(
            "Estudante não encontrado"
            ,status_code=404
        )
    
    except SQLAlchemyError:
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
        )
    

def create_estudante():
    data = request.json
    user_id = data.get("id")

    try:
        if not user_id or not Usuario.query.get(user_id):
            return APIResponse.error(
                "Usuário não existe"
                , status_code=400
            )
        
        estudante = Estudante(
            id=user_id,
            responsavel_1=data.get("responsavel_1"),
            fone_resp_1=data.get("fone_resp_1"),
            responsavel_2=data.get("responsavel_2"),
            fone_resp_2=data.get("fone_resp_2"),
            comentarios=data.get("comentarios")
        )

        db.session.add(estudante)
        db.session.commit()

        return APIResponse.success(
            "Estudante criado com sucesso"
            ,status_code=201
        )
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error(
            "Já existe um estudante para este usuário ou dados inválidos"
            ,status_code=400
        )
    
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
            )
    
def update_estudante(id):

    data = request.json
    try:
        estudante = Estudante.query.get(id)

        if not estudante:
            return APIResponse.error(
                "Estudante não encontrado"
                , status_code=404
            )
        
        est.responsavel_1 = data.get("responsavel_1", est.responsavel_1)
        est.fone_resp_1   = data.get("fone_resp_1", est.fone_resp_1)
        est.responsavel_2 = data.get("responsavel_2", est.responsavel_2)
        est.fone_resp_2   = data.get("fone_resp_2", est.fone_resp_2)
        est.comentarios   = data.get("comentarios",   est.comentarios)
        est.updated_at    = datetime.now(timezone.utc)

        db.session.commit()
        return APIResponse.success(
            "Estudante atualizado com sucesso"
        )
    
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error(
            "Dados violam restrições de integridade"
            ,status_code=400
            )
    
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados"
            , status_code=500
        )
    
def delete_estudante(id):
    try:
        estudante = Estudante.query.get(id)
        if not estudante:
            return APIResponse.error(
                "Estudante não encontrado"
                ,status_code=404
            )
        
        db.session.delete(estudante)
        db.session.commit()

        return APIResponse.success(
            "Estudante removido com sucesso."
        )
    
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
        )