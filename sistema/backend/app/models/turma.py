from datetime import datetime, timezone
from app.infra.extensions import db

class Turma(db.Model):
    __tablename__ = "turma"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)  # nome/código da turma
    sala = db.Column(db.String(50), nullable=False)        # identificador da sala

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Turma {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "sala": self.sala
        }
