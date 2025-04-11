from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    contrasenya: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    #Rel 1-M
    proyectos: Mapped[List["Proyecto"]] = relationship(back_populates="creador", cascade="all, delete-orphan")

class Proyecto(Base):
    __tablename__ = "proyecto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    #Proyecto pertenece a usuario
    creador_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    #Accedes a user desde proyectos
    creador: Mapped["User"] = relationship(back_populates="proyectos")
