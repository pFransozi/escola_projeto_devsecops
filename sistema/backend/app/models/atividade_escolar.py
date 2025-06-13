from datetime import datetime, timezone
from app.infra.extensions import db
from app.utils.encrypt_db import EncryptedField
from app.models.turma import Turma


class AtividadeEscolar(db.Model):
    __tablename__ = "atividade_escolar"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(EncryptedField(db.String(255)), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=False)

    turma = db.relationship(
        Turma, backref=db.backref("atividades_escolares", lazy="dynamic")
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<AtividadeEscolar {self.id}>"

    def to_dict(self):
        return {"id": self.id, "descricao": self.descricao, "turma_id": self.turma_id}
