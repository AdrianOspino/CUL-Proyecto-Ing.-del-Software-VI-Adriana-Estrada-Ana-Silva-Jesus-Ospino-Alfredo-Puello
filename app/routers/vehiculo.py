from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import VehiculoCreate, VehiculoUpdate, VehiculoOut
from app.db.database import get_db
from app.repository import vehiculo

router = APIRouter(
    prefix="/vehiculo",
    tags=["Vehiculos"]
)

@router.get('/v1/vehiculos', response_model=List[VehiculoOut])
def obtener_vehiculos(db: Session = Depends(get_db)):
    return vehiculo.obtener_vehiculos(db)

@router.post('/v1/crearVehiculo', response_model=VehiculoOut)
def crear_vehiculo(vehiculo_data: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo_vehiculo = vehiculo.crear_vehiculo(db, vehiculo_data)  # Corregido: llamando al repositorio
    return nuevo_vehiculo

@router.get('/v1/obtenerVehiculo/{vehiculo_id}', response_model=VehiculoOut)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    vehiculo_info = vehiculo.obtener_vehiculo(vehiculo_id, db)
    if not vehiculo_info:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo_info

@router.delete('/v1/eliminarVehiculo/{vehiculo_id}')
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    res = vehiculo.eliminar_vehiculo(vehiculo_id, db)
    if not res:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return {"respuesta": "Vehículo eliminado correctamente"}


@router.patch('/v1/actualizarVehiculo/{vehiculo_id}', response_model=VehiculoOut)
def actualizar_vehiculo(vehiculo_id: int, updateVehiculo: VehiculoUpdate, db: Session = Depends(get_db)):
    res = vehiculo.actualizar_vehiculo(vehiculo_id, updateVehiculo, db)
    if not res:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return res
