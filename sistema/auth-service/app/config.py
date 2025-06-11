import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    COGNITO_DOMAIN = os.getenv("AWS_COGNITO_DOMAIN")
    COGNITO_REGION = os.getenv("AWS_COGNITO_REGION")
    COGNITO_CLIENT_ID = os.getenv("AWS_COGNITO_CLIENT_ID")
    COGNITO_CLIENT_SECRET = os.getenv("AWS_COGNITO_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("AWS_COGNITO_REDIRECT_URI")
    TOKEN_URL = (
        f"https://{COGNITO_DOMAIN}.auth.{COGNITO_REGION}.amazoncognito.com/oauth2/token"
    )
    INTERNAL_BACKEND_URL = "https://backend:5000"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    @staticmethod
    def validate():
        if not all(
            [
                Config.COGNITO_DOMAIN,
                Config.COGNITO_CLIENT_ID,
                Config.COGNITO_CLIENT_SECRET,
                Config.REDIRECT_URI,
                Config.JWT_SECRET_KEY,  # Adicionado à validação
            ]
        ):
            raise RuntimeError(
                "Uma ou mais variáveis de ambiente do Cognito ou JWT_SECRET_KEY não foram configuradas."
            )


Config.validate()
