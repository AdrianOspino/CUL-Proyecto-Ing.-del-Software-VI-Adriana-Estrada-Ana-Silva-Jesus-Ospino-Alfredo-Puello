# app/security.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.models import Usuario
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.config import settings  # Agrega esta línea para importar la configuración

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

def create_access_token(data: dict, expires_delta: timedelta = None, secret: str = settings.SECRET_KEY):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciales de usuario no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
    if user is None:
        raise credentials_exception
    return user
