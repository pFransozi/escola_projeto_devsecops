from flask import request
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.noticia import Noticia
from app.utils.response import APIResponse

def lista_noticias():
    try:
        noticias = Noticia.query.all()
        data = [n.to_dict() for n in noticias]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def get_noticia(id):
    try:
        noticia = Noticia.query.get(id)
        if not noticia:
            return APIResponse.error("Notícia não encontrada", status_code=404)
        return APIResponse.success(data=noticia.to_dict())
    except SQLAlchemyError:
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def create_noticia():
    data = request.get_json() or {}
    required = ["descricao", "conteudo"]
    try:
        if not all(field in data for field in required):
            return APIResponse.error("Dados incompletos", status_code=400)
        nova = Noticia(
            descricao=data.get("descricao"),
            conteudo=data.get("conteudo")
        )
        db.session.add(nova)
        db.session.commit()
        return APIResponse.success("Notícia criada com sucesso!", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade ou duplicados", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def update_noticia(id):
    data = request.get_json() or {}
    try:
        noticia = Noticia.query.get(id)
        if not noticia:
            return APIResponse.error("Notícia não encontrada", status_code=404)
        noticia.descricao = data.get("descricao", noticia.descricao)
        noticia.conteudo = data.get("conteudo", noticia.conteudo)
        noticia.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return APIResponse.success("Notícia atualizada com sucesso")
    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)

def delete_noticia(id):
    try:
        noticia = Noticia.query.get(id)
        if not noticia:
            return APIResponse.error("Notícia não encontrada", status_code=404)
        db.session.delete(noticia)
        db.session.commit()
        return APIResponse.success("Notícia removida com sucesso")
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)
