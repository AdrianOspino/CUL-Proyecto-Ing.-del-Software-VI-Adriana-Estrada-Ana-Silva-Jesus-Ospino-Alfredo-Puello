from sqlalchemy.orm import Session
from app.db import models


# Crear una factura
def crear_factura(factura, db: Session):
    factura_data = factura.dict()
    nueva_factura = models.Factura(
        id_ticket=factura_data["id_ticket"],
        monto=factura_data["monto"],
        fecha_factura=factura_data.get("fecha_factura", None),
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)  # Refrescar el objeto para obtener el ID y otros campos actualizados
    return nueva_factura


# Obtener una factura por ID
def obtener_factura(factura_id: int, db: Session):
    factura = db.query(models.Factura).filter(models.Factura.id_factura == factura_id).first()
    if not factura:
        return None  # Retornar None en lugar de un mensaje de error
    return factura


# Eliminar una factura
def eliminar_factura(factura_id: int, db: Session):
    factura = db.query(models.Factura).filter(models.Factura.id_factura == factura_id).first()
    if not factura:
        return False  # Retornar False si no se encuentra la factura
    db.delete(factura)
    db.commit()
    return True  # Retornar True si la factura fue eliminada correctamente


# Obtener todas las facturas
def obtener_facturas(db: Session):
    return db.query(models.Factura).all()


# Actualizar una factura
def actualizar_factura(factura_id: int, update_factura, db: Session):
    factura = db.query(models.Factura).filter(models.Factura.id_factura == factura_id).first()
    if not factura:
        return None  # Retornar None si la factura no fue encontrada

    # Actualizar solo los campos que fueron enviados en la solicitud
    for key, value in update_factura.dict(exclude_unset=True).items():
        setattr(factura, key, value)
    
    db.commit()
    db.refresh(factura)  # Refrescar para obtener la factura actualizada
    return factura  # Retornar la factura actualizada
