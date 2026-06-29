import os
from dotenv import load_dotenv

# Charge les variables du fichier .env si présent
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'helpdesk-default-secret-key-12345')
    
    # Par défaut, utilise SQLite en local si DATABASE_URL n'est pas spécifiée
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///helpdesk.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Métadonnées de l'application
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
    APP_MESSAGE = os.environ.get('APP_MESSAGE', 'Application HelpDesk déployée automatiquement avec Jenkins')
