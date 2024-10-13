from sqlalchemy.orm import Session
from app.db import models
from app.schemas import TicketOut

# Crear un ticket
def crear_ticket(ticket_info, db: Session):
    ticket_data = ticket_info.dict()
    nuevo_ticket = models.Ticket(
        id_vehiculo=ticket_data["id_vehiculo"],
        hora_entrada=ticket_data.get("hora_entrada", None),
        hora_salida=ticket_data.get("hora_salida", None),
        tarifa=ticket_data.get("tarifa", 0),
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket

# Obtener un ticket por ID
def obtener_ticket(ticket_id: int, db: Session):
    ticket = db.query(models.Ticket).filter(models.Ticket.id_ticket == ticket_id).first()
    return ticket  # Retornar el ticket directamente

# Eliminar un ticket
def eliminar_ticket(ticket_id: int, db: Session):
    ticket = db.query(models.Ticket).filter(models.Ticket.id_ticket == ticket_id)
    if not ticket.first():
        return False  # Retornar False si no se encuentra el ticket
    ticket.delete(synchronize_session=False)
    db.commit()
    return True  # Retornar True si se eliminó correctamente

# Obtener todos los tickets
def obtener_tickets(db: Session):
    return db.query(models.Ticket).all()

# Actualizar un ticket
def actualizar_ticket(ticket_id: int, update_ticket, db: Session):
    ticket = db.query(models.Ticket).filter(models.Ticket.id_ticket == ticket_id).first()
    if not ticket:
        return None  # Retornar None si no se encuentra el ticket
    for key, value in update_ticket.dict(exclude_unset=True).items():
        setattr(ticket, key, value)  # Actualizar los campos del ticket
    db.commit()
    db.refresh(ticket)  # Refrescar el objeto
    return ticket  # Retornar el ticket actualizado
