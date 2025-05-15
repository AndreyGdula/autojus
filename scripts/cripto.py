from cryptography.fernet import Fernet
import os
import json

class Cripto:
    def __init__(self):
        self.key = self.load_key()
        self.f = Fernet(self.key)

    def load_key(self):
        key = os.environ.get("Ajcrkey")
        if not key:
            raise RuntimeError("Variável de ambiente não definida.")
        return key.encode()
        
    def save_json_cripto(self, path, data):
        json_data = json.dumps(data).encode("utf-8")
        encrypted = self.f.encrypt(json_data)
        with open(path, "wb") as file:
            file.write(encrypted)

    def load_json_cripto(self, path):
        if not path.exists():
            return {}
        with open(path, "rb") as file:
            encrypted = file.read()
        try:
            decrypted = self.f.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception:
            return {}