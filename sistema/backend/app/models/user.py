from datetime import datetime, timezone, date
from app import db
from werkzeug.security import check_password_hash
from enum import Enum
from sqlalchemy import Enum as SAEnum


class UserTipoEnum(str, Enum):
    Admin = "admin"
    Secretario = "secretario"
    Professor = "professor"


class User(db.Model):

    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    ultimo_nome = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(60), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    endereco = db.Column(db.String(255), nullable=False)

    # 0 - admin, 1-secretario, 2-professor
    tipo = db.Column(
        SAEnum(UserTipoEnum, name="user_tipo_enum", native_enum=False),
        nullable=False,
        default=UserTipoEnum.Secretario,
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    # id_user_insert = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # inserted_by = db.relationship(
    #     "User"
    #     , remote_side=[id]
    #     ,foreign_keys=[id_user_insert]
    #     , backref="inserted_users"
    # )

    # id_user_update = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # updated_by = db.relationship(
    #     "User"
    #     , remote_side=[id]
    #     ,foreign_keys=[id_user_update]
    #     , backref="updated_users"
    # )

    def __repr__(self):
        return f"<Usuário {self.usuario}>"

    def check_password(self, plain):
        return check_password_hash(self.senha, plain)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "ultimo_nome": self.ultimo_nome,
            "usuario": self.usuario,
            "email": self.email,
            "data_nascimento": self.data_nascimento,
            "sexo": self.sexo,
            "cpf": self.cpf,
            "endereco": self.endereco,
            "tipo": self.tipo,
        }
