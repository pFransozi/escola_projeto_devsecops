from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.estudante import Estudante
from app.models.usuario import Usuario
from app.utils.response import APIResponse
from datetime import datetime, timezone


def lista_estudantes():
    try:
        estudantes = Estudante.query.all()
        data = [
            {
                **e.to_dict(),
                "nome_estudante": f"{e.usuario.nome} {e.usuario.ultimo_nome}"
            }
            for e in estudantes
        ]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)


def get_estudante(id):
    try:
        estudante = Estudante.query.get(id)
        if not estudante:
            return APIResponse.error("Estudante não encontrado", status_code=404)
        data = {
            **estudante.to_dict(),
            "nome_estudante": f"{estudante.usuario.nome} {estudante.usuario.ultimo_nome}"
        }
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)


def create_estudante():
    data = request.get_json() or {}
    user_id = data.get("id")
    if not user_id or not Usuario.query.get(user_id):
        return APIResponse.error("Usuário não existe", status_code=400)
    try:
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
        return APIResponse.success("Estudante criado com sucesso", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Já existe um estudante para este usuário ou dados inválidos", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)


def update_estudante(id):
    data = request.get_json() or {}
    try:
        estudante = Estudante.query.get(id)
        if not estudante:
            return APIResponse.error("Estudante não encontrado", status_code=404)
        estudante.responsavel_1 = data.get("responsavel_1", estudante.responsavel_1)
        estudante.fone_resp_1   = data.get("fone_resp_1", estudante.fone_resp_1)
        estudante.responsavel_2 = data.get("responsavel_2", estudante.responsavel_2)
        estudante.fone_resp_2   = data.get("fone_resp_2", estudante.fone_resp_2)
        estudante.comentarios   = data.get("comentarios", estudante.comentarios)
        estudante.updated_at    = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Estudante atualizado com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)


def delete_estudante(id):
    try:
        estudante = Estudante.query.get(id)
        if not estudante:
            return APIResponse.error("Estudante não encontrado", status_code=404)
        db.session.delete(estudante)
        db.session.commit()
        return APIResponse.success("Estudante removido com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
