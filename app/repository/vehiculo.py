from sqlalchemy.orm import Session
from app.db.models import Vehiculo
from app.schemas import VehiculoCreate, VehiculoUpdate

def obtener_vehiculos(db: Session):
    return db.query(Vehiculo).all()

def crear_vehiculo(db: Session, vehiculo: VehiculoCreate):
    nuevo_vehiculo = Vehiculo(**vehiculo.dict())  # Convierte el esquema en un objeto ORM
    db.add(nuevo_vehiculo)
    db.commit()  # Guarda los cambios en la base de datos
    db.refresh(nuevo_vehiculo)  # Recarga la instancia del vehículo con los datos de la base de datos 
    return nuevo_vehiculo

def obtener_vehiculo(vehiculo_id: int, db: Session):
    return db.query(Vehiculo).filter(Vehiculo.id_vehiculo == vehiculo_id).first()

def eliminar_vehiculo(vehiculo_id: int, db: Session):
    vehiculo = obtener_vehiculo(vehiculo_id, db)
    if vehiculo:
        db.delete(vehiculo)
        db.commit()
        return True
    return False

def actualizar_vehiculo(vehiculo_id: int, update_data: VehiculoUpdate, db: Session):
    vehiculo = obtener_vehiculo(vehiculo_id, db)
    if not vehiculo:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(vehiculo, key, value)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo
