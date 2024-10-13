from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import FacturaCreate, FacturaUpdate, FacturaOut
from app.db.database import get_db
from app.repository import factura as factura_repository  # Cambiamos el alias para evitar conflictos de nombres

router = APIRouter(
    prefix="/factura",
    tags=["Facturas"]
)

# Obtener todas las facturas
@router.get('/v1/facturas', response_model=List[FacturaOut])
def obtener_facturas(db: Session = Depends(get_db)):
    return factura_repository.obtener_facturas(db)

# Crear una nueva factura
@router.post('/v1/crearFactura', response_model=FacturaOut)
def crear_factura(factura_data: FacturaCreate, db: Session = Depends(get_db)):  # Cambiamos 'factura' a 'factura_data'
    nueva_factura = factura_repository.crear_factura(factura_data, db)
    return nueva_factura

# Obtener una factura por su ID
@router.get('/v1/obtenerFactura/{factura_id}', response_model=FacturaOut)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = factura_repository.obtener_factura(factura_id, db)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

# Eliminar una factura por su ID
@router.delete('/v1/eliminarFactura/{factura_id}')
def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    res = factura_repository.eliminar_factura(factura_id, db)
    if not res:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return {"respuesta": "Factura eliminada correctamente"}

# Actualizar una factura por su ID
@router.patch('/v1/actualizarFactura/{factura_id}', response_model=FacturaOut)
def actualizar_factura(factura_id: int, updateFactura: FacturaUpdate, db: Session = Depends(get_db)):
    res = factura_repository.actualizar_factura(factura_id, updateFactura, db)
    if not res:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return res
