from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
import os

class EncryptedField(EncryptedType):
    def __init__(self, *args, **kwargs):
        secret_key = os.getenv('DB_ENCRYPTION_KEY')
        if not secret_key:
            raise ValueError("Encryption key not provided")
        # Inicializa EncryptedType com chave, engine AES e padding PKCS5
        super().__init__(*args, secret_key, AesEngine, 'pkcs5', **kwargs)