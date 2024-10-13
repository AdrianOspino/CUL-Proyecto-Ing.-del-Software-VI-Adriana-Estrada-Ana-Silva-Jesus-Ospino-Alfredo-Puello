# app/repository/user.py

from sqlalchemy.orm import Session
from app.db.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

def crear_usuario(usuario: UsuarioCreate, db: Session):
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_usuario(user_id: int, db: Session):
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

def eliminar_usuario(user_id: int, db: Session):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return {"respuesta": "Usuario eliminado correctamente"}
    return {"respuesta": "Usuario no encontrado"}

def actualizar_usuario(user_id: int, updateUser: UsuarioUpdate, db: Session):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if usuario:
        for key, value in updateUser.dict(exclude_unset=True).items():
            setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
        return usuario
    return None
