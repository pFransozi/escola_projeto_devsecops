from flask import Flask
from flask_cors import CORS
from app.infra.extensions import db, migrate
import os
from .config import config_by_name

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://myuser:mypassword@mysql_db/myappdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    # no create_app()
    CORS(
    app,
    resources={r"/api/*": {"origins": "https://localhost:3443"}},
    supports_credentials=True
    )

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  
    app.config["SESSION_COOKIE_SECURE"]   = False  # sem HTTPS local

    db.init_app(app)
    migrate.init_app(app, db)

    # with app.app_context():
    #     import app.models

    from app.middleware.auth import autenticacao

    app.before_request(autenticacao)

    from app.routes.api_bp import api_bp

    app.register_blueprint(api_bp)

    from app.routes.teste_db_routes import teste_db_bp

    app.register_blueprint(teste_db_bp)

    with app.app_context():
        from app import models

    return app
