from datetime import datetime, timezone, date
from app.infra.extensions import db
from app.utils.encrypt_db import EncryptedField
from app.models.professor import Professor
from app.models.aula import Aula

class Prova(db.Model):
    """Modelo que representa uma Prova (avaliação) aplicada em uma aula por um professor."""

    __tablename__ = "prova"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(EncryptedField(db.String(255)), nullable=False)
    data = db.Column(db.Date, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey("aula.id"), nullable=False)

    professor = db.relationship(Professor, backref=db.backref("provas", lazy="dynamic"))
    aula = db.relationship(Aula, backref=db.backref("provas", lazy="dynamic"))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Prova {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "data": self.data,
            "professor_id": self.professor_id,
            "aula_id": self.aula_id
        }
