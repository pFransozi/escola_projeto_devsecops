from app.infra.extensions import db
from app.models.usuario import Usuario
from datetime import datetime, timezone


class Professor(db.Model):

    __tablename__ = "professor"

    id = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    salario = db.Column(db.Float, nullable=False)
    graduacao = db.Column(db.String(255), nullable=True)
    descricao = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    usuario = db.relationship(Usuario, backref=db.backref("professor", uselist=False))


    def __repr__(self):
        return f"<Professor {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "salario": self.salario,
            "graduacao": self.graduacao,
            "descricao": self.descricao,
        }
