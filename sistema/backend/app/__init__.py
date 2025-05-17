from flask import Flask
from flask_cors import CORS
from app.infra.extensions import db, migrate

# db = SQLAlchemy()
# migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://myuser:mypassword@mysql_db/myappdb"
    #debug local
    #app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://myuser:mypassword@127.0.0.1:3306/myappdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.middleware.auth import autenticacao
    app.before_request(autenticacao)

    from app.routes.api_bp import api_bp
    from app.routes.usuario_routes import user_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.professor_routes import professor_bp
    from app.routes.estudante_routes import estudante_bp

    app.register_blueprint(api_bp)
    
    if "user_bp" not in api_bp._blueprints:
        api_bp.register_blueprint(user_bp, url_prefix="/usuario")
        api_bp.register_blueprint(auth_bp, url_prefix="/login")
        api_bp.register_blueprint(dashboard_bp, url_prefix="/dashboard")
        api_bp.register_blueprint(professor_bp,   url_prefix="/professor")
        api_bp.register_blueprint(estudante_bp,   url_prefix="/estudante")
    

    from app.routes.teste_db_routes import teste_db_bp
    app.register_blueprint(teste_db_bp)

    with app.app_context():
        from app import models

    return app
