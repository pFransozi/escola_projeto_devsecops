from flask import Flask
from flask_cors import CORS
from app.infra.extensions import db, migrate
import os

# db = SQLAlchemy()
# migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://myuser:mypassword@mysql_db/myappdb"
    # debug local
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://myuser:mypassword@127.0.0.1:3306/myappdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    # no create_app()
    CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
    supports_credentials=True
    )

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"   # Lax ainda envia pra top-level navigations
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
