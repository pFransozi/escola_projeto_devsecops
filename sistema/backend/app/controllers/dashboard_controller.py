from flask import jsonify
from app.models.usuario import Usuario, UsuarioTipoEnum


def dashboard_data():
    """
    Função de view para a rota do dashboard.
    Retorna dados agregados sobre usuários (total, secretários, professores, estudantes).
    Esta rota é protegida pelo decorador de permissões, requerindo usuário autenticado.
    """
    total = Usuario.query.count()
    secretarios = Usuario.query.filter_by(tipo=UsuarioTipoEnum.Secretario).count()
    professores = Usuario.query.filter_by(tipo=UsuarioTipoEnum.Professor).count()
    estudantes = Usuario.query.filter_by(tipo=UsuarioTipoEnum.Aluno).count()

    return jsonify(
        {
            "users": total,
            "secretarios": secretarios,
            "professores": professores,
            "estudantes":estudantes
        }
    )
