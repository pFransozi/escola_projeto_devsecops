from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate

# db = SQLAlchemy()
# migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://myuser:mypassword@mysql_db/myappdb"
    #debug local
    #app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://myuser:mypassword@127.0.0.1:3306/myappdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.middleware.auth import autenticacao

    app.before_request(autenticacao)

    from app.routes.user_routes import user_db

    app.register_blueprint(user_db, url_prefix="/api")

    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api")

    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(dashboard_bp, url_prefix="/api")

    from app.routes.teste_db_routes import teste_db_bp
    app.register_blueprint(teste_db_bp)

    with app.app_context():
        from app import models

    return app
