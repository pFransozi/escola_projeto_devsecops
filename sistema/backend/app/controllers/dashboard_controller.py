from flask import jsonify
from app.models.usuario import Usuario, UsuarioTipoEnum


def dashboard_data():
    total = Usuario.query.count()
    admins = Usuario.query.filter_by(tipo=UsuarioTipoEnum.Admin).count()
    secretarios = Usuario.query.filter_by(tipo=UsuarioTipoEnum.Secretario).count()
    professores = Usuario.query.filter_by(tipo=UsuarioTipoEnum.Professor).count()

    return jsonify(
        {
            "users": total,
            "admins": admins,
            "secretarios": secretarios,
            "professores": professores,
        }
    )
