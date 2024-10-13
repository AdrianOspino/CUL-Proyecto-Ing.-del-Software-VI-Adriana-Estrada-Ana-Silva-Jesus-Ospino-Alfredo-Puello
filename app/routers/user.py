# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.db.database import get_db
from app.repository import user
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models import Usuario
from app.core.config import settings  # Agrega esta línea para importar la configuración

# Define el enrutador
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# Ruta para login (sin hashing ni token)
@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Reemplaza "nuevo_usuario" y "nueva_contrasena" con los valores reales de tu .env
    db_user = settings.MYSQL_USER
    db_password = settings.MYSQL_PASSWORD

    if form_data.username != db_user or form_data.password != db_password:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return {"message": "Inicio de sesión exitoso"}

# Otras rutas de usuario...

# Ruta para obtener todos los usuarios
@router.get('/v1/usuarios', response_model=List[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    return user.obtener_usuarios(db)

# Ruta para crear un nuevo usuario
@router.post('/v1/crearUsuario', response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = user.crear_usuario(usuario, db)
    return nuevo_usuario

# Ruta para obtener un usuario específico por su ID
@router.get('/v1/obtenerUsuario/{user_id}', response_model=UsuarioOut)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = user.obtener_usuario(user_id, db)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Ruta para eliminar un usuario por su ID
@router.delete('/v1/eliminarUsuario/{user_id}')
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    res = user.eliminar_usuario(user_id, db)
    if res.get("respuesta") == "Usuario no encontrado":
        raise HTTPException(status_code=404, detail=res["respuesta"])
    return {"respuesta": res["respuesta"]}

# Ruta para actualizar un usuario
@router.patch('/v1/actualizarUsuario/{user_id}', response_model=UsuarioOut)
def actualizar_usuario(user_id: int, updateUser: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario_actualizado = user.actualizar_usuario(user_id, updateUser, db)
    if usuario_actualizado is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado
