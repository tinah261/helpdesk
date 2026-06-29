import os
import sys

# Ajoute le dossier parent au path pour s'assurer que les imports fonctionnent dans tous les contextes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app import create_app
except ImportError:
    try:
        from . import create_app
    except ImportError:
        from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    # En local, on tourne sur le port 5000 par défaut
    app.run(host='0.0.0.0', port=5000, debug=True)
