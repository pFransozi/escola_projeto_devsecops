from flask import request, g
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infra.extensions import db
from app.models.usuario import Usuario, UsuarioTipoEnum
from app.utils.response import APIResponse
from datetime import datetime

def lista_usuarios():

    """Recupera a lista de todos os usuários cadastrados no sistema."""

    try:
        usuarios = Usuario.query.all()
        data = [usuario.to_dict() for usuario in usuarios]
        return APIResponse.success(data=data)
    except SQLAlchemyError:
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
        )
    
def get_usuario(id):
    """
    Busca um usuário pelo ID fornecido.
    Parâmetros:
        id (int): O identificador único do usuário.
    Retorna:
        Resposta API JSON contendo os dados do usuário se encontrado, ou mensagem de erro 404.
    """
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return APIResponse.error(
                "Usuário não encontrado"
                , status_code=404
            )
        
        return APIResponse.success(data=usuario.to_dict())
    except SQLAlchemyError:
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
        )

def cadastrar_usuario():
    """
    Cadastra um novo usuário com base nos dados JSON fornecidos na requisição.
    Valida campos obrigatórios e unicidade do nome de usuário.
    Retorna:
        Resposta de sucesso 201 se criado ou mensagens de erro adequadas (400/500).
    """

    data = request.get_json()
    required = [
        "nome",
        "usuario",
        "senha",
        "cpf",
        "data_nascimento",
        "sexo",
        "endereco",
        "tipo",
    ]

    try:

        if not all(field in data for field in required):
            return APIResponse.error(
                "Dados incompletos"
                , status_code=400)

        if Usuario.query.filter_by(usuario=data["usuario"]).first():
            return APIResponse.error("Login já cadastrado", status_code=400)
        
        data_nascimento_raw = data.get("data_nascimento")
        try:
            data_nascimento = datetime.fromisoformat(data_nascimento_raw) if data_nascimento_raw else None
        except ValueError:
            return jsonify({"erro": "Data de nascimento inválida"}), 400

        novo_usuario = Usuario(
            nome=data["nome"],
            ultimo_nome=data["ultimo_nome"],
            usuario=data["usuario"],
            senha=generate_password_hash(data["senha"]),
            email=data.get("email"),
            data_nascimento=data_nascimento,
            sexo=data["sexo"],
            cpf=data["cpf"],
            endereco=data["endereco"],
            tipo=UsuarioTipoEnum(data["tipo"])
        )

        db.session.add(novo_usuario)
        db.session.commit()
        return APIResponse.success(
            "Usuário criado com sucesso!"
            , status_code=201)

    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)
    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error(
            "Erro interno no banco de dados"
            ,status_code=500
        )
    

def update_usuario(id):
    """
    Atualiza os dados de um usuário existente pelo ID.
    Parâmetros:
        id (int): Identificador do usuário a ser atualizado.
    Retorna:
        Resposta de sucesso com mensagem se a atualização ocorrer, ou erros 404/400/500 se falhar.
    """
    data = request.get_json()

    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return APIResponse.error("Usuário não encontrado", status_code=404)

        usuario.nome = data.get("nome", usuario.nome)
        usuario.ultimo_nome = data.get("ultimo_nome", usuario.ultimo_nome)
        if "senha" in data:
            usuario.senha = generate_password_hash(data["senha"])
        usuario.email = data.get("email", usuario.email)

        if "data_nascimento" in data:
            data_nascimento_raw = data["data_nascimento"]
            if isinstance(data_nascimento_raw, str):
                try:
                    usuario.data_nascimento = datetime.fromisoformat(data_nascimento_raw)
                except ValueError:
                    return APIResponse.error("Data de nascimento em formato inválido", status_code=400)
            elif data_nascimento_raw is None:
                usuario.data_nascimento = None
            else:
                return APIResponse.error("Data de nascimento deve ser string ou null", status_code=400)

        usuario.sexo = data.get("sexo", usuario.sexo)
        usuario.cpf = data.get("cpf", usuario.cpf)
        usuario.endereco = data.get("endereco", usuario.endereco)
        if "tipo" in data:
            usuario.tipo = UsuarioTipoEnum(data["tipo"])

        db.session.commit()
        return APIResponse.success("Usuário atualizado com sucesso")

    except IntegrityError:
        db.session.rollback()
        return APIResponse.error("Dados violam restrições de integridade", status_code=400)

    except SQLAlchemyError:
        db.session.rollback()
        return APIResponse.error("Erro interno no banco de dados", status_code=500)


def delete_usuario(id):
    """
    Remove um usuário existente pelo ID.
    Parâmetros:
        id (int): Identificador do usuário a ser removido.
    Retorna:
        Resposta de sucesso com mensagem 200 se removido, ou erro 404/500 se falhar.
    """
    try:
        user = Usuario.query.get(id)
        if not user:
            return APIResponse.error("Usuário não encontrado", status_code=404)

        db.session.delete(user)
        db.session.commit()
        return APIResponse.success("Usuário removido com sucesso")

    except Exception as e:
        db.session.rollback()
        print(f"[DELETE ERRO] {e.__class__.__name__}: {e}")
        return APIResponse.error("Erro interno no banco de dados", status_code=500)