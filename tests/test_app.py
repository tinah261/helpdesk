import os
import sys
import pytest

# Ajouter le dossier app au chemin d'importation de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Configurer les variables d'environnement de test avant d'importer create_app
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret-key-12345'
os.environ['APP_VERSION'] = '1.0.0'
os.environ['APP_MESSAGE'] = 'Application HelpDesk de test'

from app import create_app
from app.models import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Test que la page d'accueil répond avec le code 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'HelpDesk Portal' in response.data
    assert b'Application HelpDesk de test' in response.data

def test_health_check(client):
    """Test que /health répond avec le statut ok."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['version'] == '1.0.0'

def test_login_page_exists(client):
    """Test que la page login existe."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_register_page_exists(client):
    """Test que la page register existe."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Inscription' in response.data
