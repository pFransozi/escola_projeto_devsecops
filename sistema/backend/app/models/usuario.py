from datetime import datetime, timezone, date
from app.infra.extensions import db
from werkzeug.security import check_password_hash
from enum import Enum
from sqlalchemy import Enum as SAEnum


class UsuarioTipoEnum(str, Enum):
    Admin = "admin"
    Secretario = "secretario"
    Professor = "professor"
    Aluno = "aluno"


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)

    # vinculação ao Cognito
    cognito_sub = db.Column(db.String(255), unique=True, nullable=True)

    nome = db.Column(db.String(50), nullable=False)
    ultimo_nome = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    endereco = db.Column(db.String(255), nullable=False)

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

    @classmethod
    def get_by_cognito_sub_or_email(cls, sub: str, email: str):
        """
        1) Tenta buscar usuário local por cognito_sub.
        2) Se não achar, busca por email.
           - Se achar, vincula cognito_sub a esse registro.
        3) Se ainda não achar, retorna None.
        """
        user = cls.query.filter_by(cognito_sub=sub).first()
        if user:
            return user

        user = cls.query.filter_by(email=email).first()
        if user:
            user.cognito_sub = sub
            db.session.commit()
            return user

        return None

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
