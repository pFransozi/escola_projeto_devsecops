from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.atividade import Atividade
from app.utils.response import APIResponse

def lista_atividades():
    try:
        atividades = Atividade.query.all()
        data = [atividade.to_dict() for atividade in atividades]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_atividade(id):
    try:
        atividade = Atividade.query.get(id)
        if not atividade:
            return APIResponse.error("Atividade não encontrada", status_code=404)
        return APIResponse.success(data=atividade.to_dict())
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_atividade():
    data = request.get_json() or {}
    # Campos obrigatórios
    required = ["descricao", "custo", "data"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        # Converter data de string ISO para objeto date
        data_raw = data.get("data")
        try:
            data_atividade = datetime.fromisoformat(data_raw) if data_raw else None
        except ValueError:
            return APIResponse.error("Data da atividade inválida, formato esperado AAAA-MM-DD", status_code=400)
        nova = Atividade(
            descricao=data.get("descricao"),
            custo=data.get("custo"),
            data=data_atividade.date() if data_atividade else None
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Atividade criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_atividade(id):
    data = request.get_json() or {}
    try:
        atividade = Atividade.query.get(id)
        if not atividade:
            return APIResponse.error("Atividade não encontrada", status_code=404)
        # Atualiza campos se fornecidos
        atividade.descricao = data.get("descricao", atividade.descricao)
        atividade.custo = data.get("custo", atividade.custo)
        if "data" in data:
            data_raw = data.get("data")
            if isinstance(data_raw, str):
                try:
                    atividade.data = datetime.fromisoformat(data_raw).date()
                except ValueError:
                    return APIResponse.error("Data da atividade inválida", status_code=400)
            elif data_raw is None:
                atividade.data = None
            else:
                return APIResponse.error("Data da atividade em formato inválido", status_code=400)
        atividade.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Atividade atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_atividade(id):
    try:
        atividade = Atividade.query.get(id)
        if not atividade:
            return APIResponse.error("Atividade não encontrada", status_code=404)
        db.session.delete(atividade)
        db.session.commit()
        return APIResponse.success("Atividade removida com sucesso")
    except SQLAlchemyError as e:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
