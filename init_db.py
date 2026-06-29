import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

from app import create_app
from app.models import db, User

app = create_app()

with app.app_context():
    print("Création de toutes les tables de la base de données...")
    db.create_all()
    
    print("Vérification des utilisateurs par défaut...")
    
    # 1. Création du compte administrateur par défaut
    admin = User.query.filter_by(email='admin@helpdesk.local').first()
    if not admin:
        admin_pwd = generate_password_hash('admin123')
        admin = User(
            username='admin',
            email='admin@helpdesk.local',
            password_hash=admin_pwd,
            role='admin'
        )
        db.session.add(admin)
        print("Compte administrateur créé avec succès : admin@helpdesk.local / admin123")
    else:
        print("Le compte administrateur existe déjà.")
        
    # 2. Création de l'utilisateur de test par défaut
    user = User.query.filter_by(email='user@helpdesk.local').first()
    if not user:
        user_pwd = generate_password_hash('user123')
        user = User(
            username='user',
            email='user@helpdesk.local',
            password_hash=user_pwd,
            role='user'
        )
        db.session.add(user)
        print("Compte utilisateur de test créé avec succès : user@helpdesk.local / user123")
    else:
        print("Le compte utilisateur de test existe déjà.")
        
    db.session.commit()
    print("Initialisation de la base de données terminée !")
