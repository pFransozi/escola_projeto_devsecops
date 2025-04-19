from flask import jsonify
from app.models.user import User, UserTipoEnum


def dashboard_data():
    total = User.query.count()
    admins = User.query.filter_by(tipo=UserTipoEnum.Admin).count()
    secretarios = User.query.filter_by(tipo=UserTipoEnum.Secretario).count()
    professores = User.query.filter_by(tipo=UserTipoEnum.Professor).count()

    return jsonify(
        {
            "users": total,
            "admins": admins,
            "secretarios": secretarios,
            "professores": professores,
        }
    )
