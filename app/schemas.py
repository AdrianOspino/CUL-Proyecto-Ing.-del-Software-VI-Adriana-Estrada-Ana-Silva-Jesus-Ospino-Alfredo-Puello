# app/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# === Esquemas para Usuario ===

class UsuarioBase(BaseModel):
    nombre_usuario: str
    contrasena: str
    tipo_usuario: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    tipo_usuario: Optional[str] = None


class UsuarioOut(UsuarioBase):
    id_usuario: int
    creacion: datetime

    class Config:
        orm_mode = True


# === Esquemas para Vehiculo ===

class VehiculoBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: Optional[str]
    id_usuario: int


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoUpdate(BaseModel):
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    color: Optional[str] = None
    id_usuario: Optional[int] = None


class VehiculoOut(VehiculoBase):
    id_vehiculo: int

    class Config:
        orm_mode = True


# === Esquemas para Ticket ===

class TicketBase(BaseModel):
    id_vehiculo: int
    hora_entrada: str
    hora_salida: str
    tarifa: str


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    hora_entrada: Optional[str] = None
    hora_salida: Optional[str] = None
    tarifa: Optional[str] = None


class TicketOut(TicketBase):
    id_ticket: int

    class Config:
        orm_mode = True


# === Esquemas para Factura ===

class FacturaBase(BaseModel):
    id_ticket: int
    monto: str


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(BaseModel):  # Agrega esta línea
    id_ticket: Optional[int] = None
    monto: Optional[str] = None


class FacturaOut(FacturaBase):
    id_factura: int
    fecha_factura: datetime

    class Config:
        orm_mode = True


# === Esquema para Token ===
class Token(BaseModel):
    access_token: str
    token_type: str
