from datetime import datetime, timezone
from app.infra.extensions import db
from app.utils.encrypt_db import EncryptedField


class Disciplina(db.Model):

    """Modelo que representa uma Disciplina (matéria) com ementa e descrição."""

    __tablename__ = "disciplina"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(EncryptedField(db.String(255)), nullable=False)      # nome ou título da disciplina
    ementa = db.Column(db.Text, nullable=False)                # descrição longa da ementa

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Disciplina {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "ementa": self.ementa
        }
