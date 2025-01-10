import firebase_admin
from firebase_admin import credentials, auth
import os

# Inicializar Firebase Admin SDK
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "service_account.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")
