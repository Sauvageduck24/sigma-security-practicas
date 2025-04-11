from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from database import Base
from sqlalchemy import DateTime
from datetime import datetime as Datetime

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    contrasenya: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_registro: Mapped[Datetime] = mapped_column(DateTime, )
    #Rel 1-M
    proyectos: Mapped[List["Proyecto"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Proyecto(Base):
    __tablename__ = "proyecto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)
    fecha_creacion: Mapped[Datetime] = mapped_column(DateTime, )
    fecha_modificacion: Mapped[Datetime] = mapped_column(DateTime, )
    #Proyecto pertenece a usuario
    creador_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    #Accedes a user desde proyectos
    creador: Mapped["User"] = relationship(back_populates="proyectos")
    # user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

# class Address(Base):
#     __tablename__ = "address"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(100))
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

#     user: Mapped["User"] = relationship(back_populates="addresses")
