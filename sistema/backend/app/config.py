# Arquivo: sistema/backend/app/config.py
import os

class Config:
    """Configuração base."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "uma-chave-secreta-padrao")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Vamos definir a JWT_SECRET_KEY na classe base para que ambas as configs a herdem
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "uma-chave-jwt-secreta-padrao-para-testes")

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://myuser:mypassword@mysql_db/myappdb"

class TestingConfig(Config):
    """Configuração de teste."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # A JWT_SECRET_KEY é herdada da classe Config base. Nenhuma alteração extra é necessária aqui.


# Dicionário para facilitar a seleção da configuração
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}