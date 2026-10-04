from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

#Tabla de juegos
class JuegoDB(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    genero = Column(String)
    plataforma = Column(String)
    dificultad = Column(String)
    año = Column(Integer)
    puntuacion = Column(Float)


#Tabla de usuarios
class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)


#Tabla de favoritos
class FavoritoDB(Base):
    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    juego_id = Column(Integer, ForeignKey("juegos.id"))