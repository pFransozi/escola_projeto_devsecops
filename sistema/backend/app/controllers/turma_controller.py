from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.turma import Turma
from app.utils.response import APIResponse

def lista_turmas():
    try:
        turmas = Turma.query.all()
        data = [t.to_dict() for t in turmas]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_turma(id):
    try:
        turma = Turma.query.get(id)
        if not turma:
            return APIResponse.error("Turma não encontrada", status_code=404)
        return APIResponse.success(data=turma.to_dict())
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_turma():
    data = request.get_json() or {}
    required = ["descricao", "sala"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        nova = Turma(
            descricao=data.get("descricao"),
            sala=data.get("sala")
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Turma criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_turma(id):
    data = request.get_json() or {}
    try:
        turma = Turma.query.get(id)
        if not turma:
            return APIResponse.error("Turma não encontrada", status_code=404)
        turma.descricao = data.get("descricao", turma.descricao)
        turma.sala = data.get("sala", turma.sala)
        turma.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Turma atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_turma(id):
    try:
        turma = Turma.query.get(id)
        if not turma:
            return APIResponse.error("Turma não encontrada", status_code=404)
        db.session.delete(turma)
        db.session.commit()
        return APIResponse.success("Turma removida com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
