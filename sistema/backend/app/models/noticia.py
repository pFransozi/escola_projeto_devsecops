from datetime import datetime, timezone
from app.infra.extensions import db
from app.utils.encrypt_db import EncryptedField

class Noticia(db.Model):

    """Modelo que representa uma Notícia publicada para o sistema escolar."""

    __tablename__ = "noticia"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(EncryptedField(db.String(255)), nullable=False)  # título ou chamada da notícia
    conteudo = db.Column(EncryptedField(db.Text), nullable=False)          # texto completo da notícia

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Noticia {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "conteudo": self.conteudo
        }
