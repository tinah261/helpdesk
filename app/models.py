from datetime import datetime, timezone
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' ou 'user'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relation
    tickets = db.relationship('Ticket', backref='author', lazy=True)
    
    def is_admin(self):
        return self.role == 'admin'

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'Réseau', 'Matériel', 'Logiciel', 'Compte utilisateur', 'Autre'
    priority = db.Column(db.String(20), default='Moyenne', nullable=False)  # 'Faible', 'Moyenne', 'Haute', 'Urgente'
    status = db.Column(db.String(20), default='Ouvert', nullable=False)  # 'Ouvert', 'En cours', 'Résolu', 'Fermé'
    admin_response = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
