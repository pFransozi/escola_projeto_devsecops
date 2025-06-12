from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.atividade_escolar import AtividadeEscolar
from app.models.turma import Turma
from app.utils.response import APIResponse

def lista_atividades_escolares():
    try:
        atividades = AtividadeEscolar.query.all()
        data = [
            { **ativ.to_dict(),
              "turma_descricao": ativ.turma.descricao if ativ.turma else None
            }
            for ativ in atividades
        ]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_atividade_escolar(id):
    try:
        ativ = AtividadeEscolar.query.get(id)
        if not ativ:
            return APIResponse.error("Atividade escolar não encontrada", status_code=404)
        data = {
            **ativ.to_dict(),
            "turma_descricao": ativ.turma.descricao if ativ.turma else None
        }
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_atividade_escolar():
    data = request.get_json() or {}
    required = ["descricao", "turma_id"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        turma_id = data.get("turma_id")
        if not turma_id or not Turma.query.get(turma_id):
            return APIResponse.error("Turma especificada não existe", status_code=400)
        nova = AtividadeEscolar(
            descricao=data.get("descricao"),
            turma_id=turma_id
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Atividade escolar criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_atividade_escolar(id):
    data = request.get_json() or {}
    try:
        ativ = AtividadeEscolar.query.get(id)
        if not ativ:
            return APIResponse.error("Atividade escolar não encontrada", status_code=404)
        if "turma_id" in data:
            turma_id = data.get("turma_id")
            if turma_id and not Turma.query.get(turma_id):
                return APIResponse.error("Turma especificada não existe", status_code=400)
            ativ.turma_id = turma_id if turma_id else ativ.turma_id
        ativ.descricao = data.get("descricao", ativ.descricao)
        ativ.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Atividade escolar atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_atividade_escolar(id):
    try:
        ativ = AtividadeEscolar.query.get(id)
        if not ativ:
            return APIResponse.error("Atividade escolar não encontrada", status_code=404)
        db.session.delete(ativ)
        db.session.commit()
        return APIResponse.success("Atividade escolar removida com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
