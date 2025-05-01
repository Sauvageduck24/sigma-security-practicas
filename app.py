import sys
import os

# Agrega el path de tu proyecto
path = '/home/sauvageduck24/sigma-security-practicas'
if path not in sys.path:
    sys.path.append(path)

# Importa la app de Flask
from app import app as application

application.run(port=5000, debug=True)