from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.disciplina import Disciplina
from app.utils.response import APIResponse

def lista_disciplinas():
    try:
        disciplinas = Disciplina.query.all()
        data = [disc.to_dict() for disc in disciplinas]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_disciplina(id):
    try:
        disc = Disciplina.query.get(id)
        if not disc:
            return APIResponse.error("Disciplina não encontrada", status_code=404)
        return APIResponse.success(data=disc.to_dict())
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_disciplina():
    data = request.get_json() or {}
    required = ["descricao", "ementa"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        nova = Disciplina(
            descricao=data.get("descricao"),
            ementa=data.get("ementa")
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Disciplina criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_disciplina(id):
    data = request.get_json() or {}
    try:
        disc = Disciplina.query.get(id)
        if not disc:
            return APIResponse.error("Disciplina não encontrada", status_code=404)
        disc.descricao = data.get("descricao", disc.descricao)
        disc.ementa = data.get("ementa", disc.ementa)
        disc.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Disciplina atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_disciplina(id):
    try:
        disc = Disciplina.query.get(id)
        if not disc:
            return APIResponse.error("Disciplina não encontrada", status_code=404)
        db.session.delete(disc)
        db.session.commit()
        return APIResponse.success("Disciplina removida com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
