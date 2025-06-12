from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.aula import Aula
from app.models.professor import Professor
from app.models.turma import Turma
from app.utils.response import APIResponse

def lista_aulas():
    try:
        aulas = Aula.query.all()
        data = [
            {
                **aula.to_dict(),
                "nome_professor": f"{aula.professor.usuario.nome} {aula.professor.usuario.ultimo_nome}" if aula.professor and aula.professor.usuario else None,
                "turma_descricao": aula.turma.descricao if aula.turma else None
            }
            for aula in aulas
        ]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_aula(id):
    try:
        aula = Aula.query.get(id)
        if not aula:
            return APIResponse.error("Aula não encontrada", status_code=404)
        data = {
            **aula.to_dict(),
            "nome_professor": f"{aula.professor.usuario.nome} {aula.professor.usuario.ultimo_nome}" if aula.professor and aula.professor.usuario else None,
            "turma_descricao": aula.turma.descricao if aula.turma else None
        }
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_aula():
    data = request.get_json() or {}
    required = ["descricao", "professor_id", "turma_id"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        prof_id = data.get("professor_id")
        turma_id = data.get("turma_id")
        if not prof_id or not Professor.query.get(prof_id):
            return APIResponse.error("Professor especificado não existe", status_code=400)
        if not turma_id or not Turma.query.get(turma_id):
            return APIResponse.error("Turma especificada não existe", status_code=400)
        nova = Aula(
            descricao=data.get("descricao"),
            professor_id=prof_id,
            turma_id=turma_id
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Aula criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_aula(id):
    data = request.get_json() or {}
    try:
        aula = Aula.query.get(id)
        if not aula:
            return APIResponse.error("Aula não encontrada", status_code=404)
        # Se for atualizar professor ou turma, checar existência
        if "professor_id" in data:
            prof_id = data.get("professor_id")
            if prof_id and not Professor.query.get(prof_id):
                return APIResponse.error("Professor especificado não existe", status_code=400)
            aula.professor_id = prof_id if prof_id else aula.professor_id
        if "turma_id" in data:
            turma_id = data.get("turma_id")
            if turma_id and not Turma.query.get(turma_id):
                return APIResponse.error("Turma especificada não existe", status_code=400)
            aula.turma_id = turma_id if turma_id else aula.turma_id
        aula.descricao = data.get("descricao", aula.descricao)
        aula.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Aula atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_aula(id):
    try:
        aula = Aula.query.get(id)
        if not aula:
            return APIResponse.error("Aula não encontrada", status_code=404)
        db.session.delete(aula)
        db.session.commit()
        return APIResponse.success("Aula removida com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
