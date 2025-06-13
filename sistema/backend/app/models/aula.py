from datetime import datetime, timezone
from app.infra.extensions import db
from app.utils.encrypt_db import EncryptedField
from app.models.professor import Professor
from app.models.turma import Turma

class Aula(db.Model):

    """Modelo que representa uma Aula, contendo descrição, professor e turma associados."""

    __tablename__ = "aula"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(EncryptedField(db.String(255)), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=False)

    professor = db.relationship(Professor, backref=db.backref("aulas", lazy="dynamic"))
    turma = db.relationship(Turma, backref=db.backref("aulas", lazy="dynamic"))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Aula {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "turma_id": self.turma_id
        }
