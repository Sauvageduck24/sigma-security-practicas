from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_praetorian import Praetorian
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime

load_dotenv()

# Para Flask
db = SQLAlchemy()

entorno = os.getenv('ENTORNO', 'local')

#uri = 'mysql+pymysql://sauvageduck24:sigmasecurity@sauvageduck24.mysql.pythonanywhere-services.com/sauvageduck24$sigmasecurity'
uri = 'mysql+pymysql://root:1234@localhost/sigma_security'

engine = create_engine(uri)

class User(db.Model):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # Este será tu "username"
    contrasenya: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    proyectos: Mapped[List["Proyecto"]] = relationship(back_populates="creador", cascade="all, delete-orphan")

    # Requerido por Flask-Praetorian:
    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(nombre=username).first()

    def identity(self):
        return self.id

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    # Esto le dice a Praetorian qué campo contiene la contraseña
    @property
    def rolenames(self):
        return []  # O una lista con roles si los usas

    @property
    def password(self):
        return self.contrasenya

class Proyecto(db.Model):
    __tablename__ = "proyecto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #Proyecto pertenece a usuario
    creador_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    #Accedes a user desde proyectos
    creador: Mapped["User"] = relationship(back_populates="proyectos")
    mensajes: Mapped[List["Mensaje"]] = relationship(back_populates="proyecto", cascade="all, delete-orphan") #mensajes de un proyecto

class Mensaje(db.Model):
    __tablename__ = "mensajes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contenido: Mapped[str] = mapped_column(String(500), nullable=False)

    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyecto.id"), nullable=False)
    proyecto: Mapped["Proyecto"] = relationship(back_populates="mensajes")

    usuario_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    usuario: Mapped["User"] = relationship()

def comprobar_y_crear_tablas():
    inspector = inspect(engine)
    tablas_existentes = inspector.get_table_names()

    tablas_objetivo = {
        "user_account": User,
        "proyecto": Proyecto,
        "mensajes": Mensaje
    }

    tablas_a_crear = []

    for nombre_tabla, modelo in tablas_objetivo.items():
        if nombre_tabla not in tablas_existentes:
            print(f"Tabla '{nombre_tabla}' no existe. Se marcará para creación.")
            tablas_a_crear.append(modelo)
        else:
            print(f"Tabla '{nombre_tabla}' ya existe.")

    if tablas_a_crear:
        print("Creando tablas necesarias...")
        db.Model.metadata.create_all(engine, tables=[modelo.__table__ for modelo in tablas_a_crear])
        print("Tablas creadas.")
    else:
        print("No hay tablas nuevas para crear.")

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Llamamos a la función para comprobar y crear las tablas al conectar
    comprobar_y_crear_tablas()  # Esto se ejecuta cada vez que inicies la conexión