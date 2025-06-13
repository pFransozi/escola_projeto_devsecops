import os

class Config:
    """Configuração base da aplicação."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "uma-chave-secreta-padrao")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Vamos definir a JWT_SECRET_KEY na classe base para que ambas as configs a herdem
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "uma-chave-jwt-secreta-padrao-para-testes")

class DevelopmentConfig(Config):
    """Configuração específica para ambiente de desenvolvimento."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://myuser:mypassword@mysql_db/myappdb"

class TestingConfig(Config):
    """Configuração específica para ambiente de testes (testes unitários)."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Dicionário para facilitar a seleção da configuração
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}