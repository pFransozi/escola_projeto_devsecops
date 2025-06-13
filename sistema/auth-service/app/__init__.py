from flask import Flask
from .config import Config

def create_app():
    """Cria e configura a aplicação Flask do Auth Service, registrando o blueprint de autenticação."""

    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app