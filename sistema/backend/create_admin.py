from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.user import User, UserTipoEnum

app = create_app()

usuarios_iniciais = [
    {
        "nome": "Carlos",
        "ultimo_nome": "Bonomini",
        "usuario": "admin",
        "senha": "admin123",
        "email": "carlos@escola.com.br",
        "data_nascimento": "1986-01-04",
        "sexo": "M",
        "cpf": "00000000032",
        "endereco": "Escola I",
        "tipo": UserTipoEnum.Admin,
    }
]

with app.app_context():
    for user in usuarios_iniciais:
        if User.query.filter_by(usuario=user["usuario"]).first():
            print("Admin já existe. Nenhuma ação necessária")
            continue

        novo_user = User(
            nome=user["nome"],
            ultimo_nome=user["ultimo_nome"],
            usuario=user["usuario"],
            senha=generate_password_hash(user["senha"]),
            email=user["email"],
            data_nascimento=user["data_nascimento"],
            sexo=user["sexo"],
            cpf=user["cpf"],
            endereco=user["endereco"],
            tipo=user["tipo"],
            # id_user_insert=0,  # se necessário, atualize depois
            # id_user_update=0,
        )

        db.session.add(novo_user)
        print(f"Usuário '{user['usuario']}' criado.")

    try:
        db.session.commit()
        print("Todos os usuários foram criados com sucesso.")
    except Exception as e:
        db.session.rollback()
        print("Erro ao salvar usuários:", str(e))
