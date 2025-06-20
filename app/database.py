from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_praetorian import Praetorian
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime,Column, Text
from datetime import datetime, timezone
from api.engine import engine,uri
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import LONGTEXT

load_dotenv()

# Para Flask
db = SQLAlchemy()

entorno = os.getenv('ENTORNO', 'local')

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "sigma_security")
uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

class User(db.Model):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)  # Este es el username
    contrasenya = Column(String(200), nullable=False)
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    proyectos = relationship("Proyecto", back_populates="creador", cascade="all, delete-orphan")

    # 🔐 Requerido por Flask-Praetorian
    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(nombre=username).first()

    def identify(self):
        return self.id

    @property
    def identity(self):
        return self.id  # <- ✅ Esta línea soluciona el error

    @property
    def rolenames(self):
        return ["admin"] if self.nombre == "admin" else ["usuario"]

    @property
    def password(self):
        return self.contrasenya

class Proyecto(db.Model):
    __tablename__ = "proyecto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    sbom: Mapped[str] = mapped_column(LONGTEXT, nullable=True)  # Nuevo campo para SBOM
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