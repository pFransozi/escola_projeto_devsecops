from app.infra.extensions import db
from app.models.usuario import Usuario
from datetime import datetime, timezone
from app.utils.encrypt_db import EncryptedField


class Estudante(db.Model):
    
    __tablename__ = "estudante"

    id = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    responsavel_1 = db.Column(EncryptedField(db.String(50)), nullable=True)
    fone_resp_1 = db.Column(EncryptedField(db.String(18)), nullable=True)
    responsavel_2 = db.Column(EncryptedField(db.String(50)), nullable=True)
    fone_resp_2 = db.Column(EncryptedField(db.String(18)), nullable=True)
    comentarios = db.Column(EncryptedField(db.String(255)), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    usuario = db.relationship(Usuario, backref=db.backref("estudante", uselist=False))

    def __repr__(self):
        return f"<Aluno {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "responsavel_1": self.responsavel_1,
            "fone_resp_1":self.fone_resp_1,
            "responsavel_2":self.responsavel_2,
            "fone_resp_2":self.fone_resp_2,

        }

