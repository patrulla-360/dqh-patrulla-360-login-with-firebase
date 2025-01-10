import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyDnSFWEJ1A58r6uieJFNfW-XX44ZPIZ10Y")
CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "service_account.json")
