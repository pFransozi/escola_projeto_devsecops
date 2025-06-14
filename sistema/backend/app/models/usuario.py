from datetime import datetime, timezone, date
from app.infra.extensions import db
from app.utils.encrypt_db import EncryptedField
from werkzeug.security import check_password_hash
from enum import Enum
from sqlalchemy import Enum as SAEnum


class UsuarioTipoEnum(str, Enum):
    """Enumeração dos tipos de usuário no sistema."""

    Secretario = "secretario"
    Professor = "professor"
    Aluno = "aluno"


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(EncryptedField(db.String(50)), nullable=False)
    ultimo_nome = db.Column(EncryptedField(db.String(50)), nullable=False)
    usuario = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(EncryptedField(db.String(60)), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    cpf = db.Column(EncryptedField(db.String(11)), nullable=False) #unique=True
    endereco = db.Column(EncryptedField(db.String(255)), nullable=False)

    # 0 - admin, 1-secretario, 2-professor
    tipo = db.Column(
        SAEnum(UsuarioTipoEnum, name="user_tipo_enum", native_enum=False),
        nullable=False,
        default=UsuarioTipoEnum.Secretario,
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=None, onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Usuário {self.usuario}>"

    def check_password(self, plain):
        """
        Verifica se a senha fornecida corresponde à senha armazenada.
        Parâmetros:
            plain (str): Senha em texto plano para verificação.
        Retorna:
            bool: True se a senha estiver correta, False caso contrário.
        """
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
