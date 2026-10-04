from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


#Tablas de la BD---------------------------------------------------------------------------------------------------------

# Tabla de Juegos
class Juego(BaseModel):
    nombre: str
    genero: str
    plataforma: str
    dificultad: str
    año: int
    puntuacion: float
   
#Tabla de usuarios    
class Usuario(BaseModel):
    nombre: str
    email: str


#Endpoints--------------------------------------------------------------------------------------------------------------

#Inicio
@app.get("/")
def inicio():
    return {"mensaje": "Hola usuario, este es el inicio"}

# ENDPOINTS DE JUEGOS

#Filtra y muestra los juegos de la BD
@app.get("/juegos")
def obtener_juegos(
    genero: str = None,
    plataforma: str = None,
    dificultad: str = None,
    año: int = None,
    puntuacion: float = None,
    db: Session = Depends(get_db)
):
    consulta = db.query(models.JuegoDB)

    if genero:
        consulta = consulta.filter(models.JuegoDB.genero == genero)

    if plataforma:
        consulta = consulta.filter(models.JuegoDB.plataforma == plataforma)

    if dificultad:
        consulta = consulta.filter(models.JuegoDB.dificultad == dificultad)

    if año:
        consulta = consulta.filter(models.JuegoDB.año == año)

    if puntuacion:
        consulta = consulta.filter(models.JuegoDB.puntuacion >= puntuacion)

    return consulta.all()


#Añade un juego a la BD
@app.post("/juegos")
def crear_juego(juego: Juego, db: Session = Depends(get_db)):
    nuevo_juego = models.JuegoDB(
        nombre=juego.nombre,
        genero=juego.genero,
        plataforma=juego.plataforma,
        dificultad=juego.dificultad,
        año=juego.año,
        puntuacion=juego.puntuacion
    )

    db.add(nuevo_juego)
    db.commit()
    db.refresh(nuevo_juego)

    return nuevo_juego


#Muestra el juego por id
@app.get("/juegos/{juego_id}")
def obtener_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(models.JuegoDB).filter(models.JuegoDB.id == juego_id).first()

    if juego is None:
        raise HTTPException(
            status_code=404,
            detail="Juego no encontrado"
            )

    return juego


#Modifica atributos de un juego de la BD
@app.put("/juegos/{juego_id}")
def actualizar_juego(
    juego_id: int,
    juego_actualizado: Juego,
    db: Session = Depends(get_db)
):
    juego = db.query(models.JuegoDB).filter(
        models.JuegoDB.id == juego_id
    ).first()

    if juego is None:
        raise HTTPException(
            status_code=404,
            detail="Juego no encontrado"
            )

    juego.nombre = juego_actualizado.nombre
    juego.genero = juego_actualizado.genero
    juego.plataforma = juego_actualizado.plataforma
    juego.dificultad = juego_actualizado.dificultad
    juego.año = juego_actualizado.año
    juego.puntuacion = juego_actualizado.puntuacion

    db.commit()
    db.refresh(juego)

    return juego


#Elimina un juego de la BD
@app.delete("/juegos/{juego_id}")
def eliminar_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(models.JuegoDB).filter(
        models.JuegoDB.id == juego_id
    ).first()

    if juego is None:
        raise HTTPException(
            status_code=404,
            detail="Juego no encontrado"
            )

    db.delete(juego)
    db.commit()

    return {"mensaje": "Juego eliminado correctamente"}


# ENDPOINTS DE USUARIOS


#Añade un usuario a la BD 
@app.post("/usuarios")
def crear_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    nuevo_usuario = models.UsuarioDB(
        nombre=usuario.nombre,
        email=usuario.email
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


#Muestra todos los usuarios de la BD
@app.get("/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.UsuarioDB).all()

    return usuarios


#Muestra usuario por id
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.UsuarioDB).filter(
        models.UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
            )

    return usuario


#Modifica atributos de un usuario de la BD
@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(
    usuario_id: int,
    usuario_actualizado: Usuario,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.UsuarioDB).filter(
        models.UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
            )

    usuario.nombre = usuario_actualizado.nombre
    usuario.email = usuario_actualizado.email

    db.commit()
    db.refresh(usuario)

    return usuario


#Elimina un usuario de la BD
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.UsuarioDB).filter(
        models.UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
            )

    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado correctamente"}


# ENDPOINTS DE FAVORITOS


#Agrega una fila a la tabla Favorito (con un usuario de la tabla Usuario y un juego de la tabla Juego)
@app.post("/usuarios/{usuario_id}/favoritos/{juego_id}")
def agregar_favorito(
    usuario_id: int,
    juego_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.UsuarioDB).filter(
        models.UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="usuario no encontrado"
            )

    juego = db.query(models.JuegoDB).filter(
        models.JuegoDB.id == juego_id
    ).first()

    if juego is None:
        raise HTTPException(
            status_code=404,
            detail="Juego no encontrado"
            )
    
    favorito_existente = db.query(models.FavoritoDB).filter(
        models.FavoritoDB.usuario_id == usuario_id,
        models.FavoritoDB.juego_id == juego_id
    ).first()

    if favorito_existente:
        raise HTTPException(
            status_code=409,
            detail="El juego ya está en favoritos"
        )


    favorito = models.FavoritoDB(
        usuario_id=usuario_id,
        juego_id=juego_id
    )

    db.add(favorito)
    db.commit()
    db.refresh(favorito)

    return favorito


#Muestra los favoritos de un usuario
@app.get("/usuarios/{usuario_id}/favoritos")
def obtener_favoritos(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.UsuarioDB).filter(
        models.UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
            )

    favoritos = db.query(models.FavoritoDB).filter(
        models.FavoritoDB.usuario_id == usuario_id
    ).all()

    return favoritos


#Elimina una fila de la tabla Favorito (con los parametros de id de usuario y de juego)
@app.delete("/usuarios/{usuario_id}/favoritos/{juego_id}")
def eliminar_favorito(
    usuario_id: int,
    juego_id: int,
    db: Session = Depends(get_db)
):
    favorito = db.query(models.FavoritoDB).filter(
        models.FavoritoDB.usuario_id == usuario_id,
        models.FavoritoDB.juego_id == juego_id
    ).first()

    if favorito is None:
        raise HTTPException(
            status_code=404,
            detail="Favorito no encontrado"
            )

    db.delete(favorito)
    db.commit()

    return {"mensaje": "Favorito eliminado correctamente"}



#  SISTEMA DE RECOMENDACIONES


@app.get("/usuarios/{usuario_id}/recomendaciones")
def obtener_recomendaciones(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.UsuarioDB).filter(
        models.UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
            )

    favoritos = db.query(models.FavoritoDB).filter(
        models.FavoritoDB.usuario_id == usuario_id
    ).all()

    if not favoritos:
        return {"mensaje": "El usuario no tiene favoritos"}

    juegos_favoritos = []

    for favorito in favoritos:
        juego = db.query(models.JuegoDB).filter(
            models.JuegoDB.id == favorito.juego_id
        ).first()

        if juego:
            juegos_favoritos.append(juego)

    ids_favoritos = [juego.id for juego in juegos_favoritos]

    todos_los_juegos = db.query(models.JuegoDB).all()

    recomendaciones = []

    for juego in todos_los_juegos:

        if juego.id in ids_favoritos:
            continue

        mejor_relevancia = 0

        for favorito in juegos_favoritos:

            relevancia = 0

            if juego.genero == favorito.genero:
                relevancia += 100

            if juego.plataforma == favorito.plataforma:
                relevancia += 10

            if juego.dificultad == favorito.dificultad:
                relevancia += 1

            if relevancia > mejor_relevancia:
                mejor_relevancia = relevancia

        recomendaciones.append({
            "juego": juego,
            "relevancia": mejor_relevancia
        })

    recomendaciones.sort(
        key=lambda x: (x["relevancia"], x["juego"].puntuacion),
        reverse=True
    )

    return recomendaciones