from datetime import datetime, timezone, date
from app.infra.extensions import db

class Atividade(db.Model):
    __tablename__ = "atividade"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    custo = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Atividade {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "custo": self.custo,
            "data": self.data
        }
