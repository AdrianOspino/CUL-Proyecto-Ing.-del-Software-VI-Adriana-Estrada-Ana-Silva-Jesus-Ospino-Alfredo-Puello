from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, Enum, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

# Tabla Usuario
class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(255), unique=True)
    contrasena = Column(String(255))  
    tipo_usuario = Column(String(255)) 
    creacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    estado = Column(Boolean, default=True)
    
    # Relación con la tabla Vehiculo
    vehiculos = relationship("Vehiculo", backref="usuario", cascade="all, delete-orphan")

# Tabla Vehiculo
class Vehiculo(Base):
    __tablename__ = "vehiculo"
    id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)  # Se cambió 'id' por 'id_vehiculo'
    placa = Column(String(250), unique=True, nullable=False)
    marca = Column(String(255))
    modelo = Column(String(250))
    color = Column(String(250))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"))  # Asegúrate que el FK coincida

    # Relación con la tabla Ticket
    tickets = relationship("Ticket", backref="vehiculo", cascade="all, delete-orphan")


# Tabla Ticket
class Ticket(Base):
    __tablename__ = "ticket"
    id_ticket = Column(Integer, primary_key=True, autoincrement=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculo.id_vehiculo", ondelete="CASCADE"), nullable=False)
    hora_entrada = Column(String(250))
    hora_salida = Column(String(250))
    tarifa = Column(String(250))

    # Relación con la tabla Factura
    factura = relationship("Factura", backref="ticket", cascade="all, delete-orphan", uselist=False)

# Tabla Factura
class Factura(Base):
    __tablename__ = "factura"
    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_ticket = Column(Integer, ForeignKey("ticket.id_ticket", ondelete="CASCADE"), nullable=False)
    monto = Column(String(250))
    fecha_factura = Column(DateTime, default=datetime.now)

        
