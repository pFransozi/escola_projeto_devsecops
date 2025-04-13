import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.getenv('DB_USER', 'myuser')}:"
        f"{os.getenv('DB_PASSWORD', 'mypassword')}@"
        f"{os.getenv('DB_HOST', 'mysql_db')}/"
        f"{os.getenv('DB_NAME', 'myappdb')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False