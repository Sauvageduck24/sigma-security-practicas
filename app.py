import sys
import os

# Agrega el path de tu proyecto
path = '/home/sauvageduck24/sigma-security-practicas'
if path not in sys.path:
    sys.path.append(path)

# Importa la app de Flask
from app import application

application.run(host="0.0.0.0", port=5000, debug=True)