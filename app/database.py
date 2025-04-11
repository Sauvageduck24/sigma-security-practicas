from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    entorno = os.getenv('ENTORNO', 'local')  # 'local' o 'produccion'

    if entorno == 'produccion':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:clave@usuario.mysql.pythonanywhere-services.com/nombre_db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:clave@localhost/nombre_db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)