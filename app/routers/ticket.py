from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import TicketCreate, TicketUpdate, TicketOut
from app.db.database import get_db
from app.repository import ticket

router = APIRouter(
    prefix="/ticket",
    tags=["Tickets"]
)

# Obtener todos los tickets
@router.get('/v1/tickets', response_model=List[TicketOut])
def obtener_tickets(db: Session = Depends(get_db)):
    return ticket.obtener_tickets(db)

# Crear un ticket
@router.post('/v1/crearTicket', response_model=TicketOut)
def crear_ticket(ticket_info: TicketCreate, db: Session = Depends(get_db)):
    nuevo_ticket = ticket.crear_ticket(ticket_info, db)
    return nuevo_ticket

# Obtener un ticket por ID
@router.get('/v1/obtenerTicket/{ticket_id}', response_model=TicketOut)
def obtener_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket_obtenido = ticket.obtener_ticket(ticket_id, db)
    if not ticket_obtenido:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket_obtenido

# Eliminar un ticket
@router.delete('/v1/eliminarTicket/{ticket_id}')
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    eliminado = ticket.eliminar_ticket(ticket_id, db)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return {"respuesta": "Ticket eliminado correctamente"}

# Actualizar un ticket
@router.patch('/v1/actualizarTicket/{ticket_id}', response_model=TicketOut)
def actualizar_ticket(ticket_id: int, updateTicket: TicketUpdate, db: Session = Depends(get_db)):
    ticket_actualizado = ticket.actualizar_ticket(ticket_id, updateTicket, db)
    if ticket_actualizado is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket_actualizado
