from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.prova import Prova
from app.models.professor import Professor
from app.models.aula import Aula
from app.utils.response import APIResponse

def lista_provas():
    try:
        provas = Prova.query.all()
        data = [
            {
                **prova.to_dict(),
                "nome_professor": f"{prova.professor.usuario.nome} {prova.professor.usuario.ultimo_nome}" if prova.professor and prova.professor.usuario else None,
                "aula_descricao": prova.aula.descricao if prova.aula else None,
                "turma_descricao": prova.aula.turma.descricao if prova.aula and prova.aula.turma else None
            }
            for prova in provas
        ]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_prova(id):
    try:
        prova = Prova.query.get(id)
        if not prova:
            return APIResponse.error("Prova não encontrada", status_code=404)
        data = {
            **prova.to_dict(),
            "nome_professor": f"{prova.professor.usuario.nome} {prova.professor.usuario.ultimo_nome}" if prova.professor and prova.professor.usuario else None,
            "aula_descricao": prova.aula.descricao if prova.aula else None,
            "turma_descricao": prova.aula.turma.descricao if prova.aula and prova.aula.turma else None
        }
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_prova():
    data = request.get_json() or {}
    required = ["descricao", "data", "professor_id", "aula_id"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        prof_id = data.get("professor_id")
        aula_id = data.get("aula_id")
        if not prof_id or not Professor.query.get(prof_id):
            return APIResponse.error("Professor especificado não existe", status_code=400)
        if not aula_id or not Aula.query.get(aula_id):
            return APIResponse.error("Aula especificada não existe", status_code=400)
        # Converter data string para date
        data_raw = data.get("data")
        try:
            data_prova = datetime.fromisoformat(data_raw) if data_raw else None
        except ValueError:
            return APIResponse.error("Data da prova inválida, formato esperado AAAA-MM-DD", status_code=400)
        nova = Prova(
            descricao=data.get("descricao"),
            data=data_prova.date() if data_prova else None,
            professor_id=prof_id,
            aula_id=aula_id
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Prova criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_prova(id):
    data = request.get_json() or {}
    try:
        prova = Prova.query.get(id)
        if not prova:
            return APIResponse.error("Prova não encontrada", status_code=404)
        if "professor_id" in data:
            prof_id = data.get("professor_id")
            if prof_id and not Professor.query.get(prof_id):
                return APIResponse.error("Professor especificado não existe", status_code=400)
            prova.professor_id = prof_id if prof_id else prova.professor_id
        if "aula_id" in data:
            aula_id = data.get("aula_id")
            if aula_id and not Aula.query.get(aula_id):
                return APIResponse.error("Aula especificada não existe", status_code=400)
            prova.aula_id = aula_id if aula_id else prova.aula_id
        if "data" in data:
            data_raw = data.get("data")
            if isinstance(data_raw, str):
                
                try:
                    prova.data = datetime.fromisoformat(data_raw).date()
                except ValueError:
                    return APIResponse.error("Data da prova inválida", status_code=400)
            
            elif data_raw is None:
                prova.data = None
            else:
                return APIResponse.error("Data da prova em formato inválido", status_code=400)
        prova.descricao = data.get("descricao", prova.descricao)
        prova.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Prova atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_prova(id):
    try:
        prova = Prova.query.get(id)
        if not prova:
            return APIResponse.error("Prova não encontrada", status_code=404)
        db.session.delete(prova)
        db.session.commit()
        return APIResponse.success("Prova removida com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
