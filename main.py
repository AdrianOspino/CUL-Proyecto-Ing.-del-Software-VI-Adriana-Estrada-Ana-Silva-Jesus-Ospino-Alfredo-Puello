from fastapi import FastAPI, Request
from dotenv import load_dotenv
from pathlib import Path
from app.routers.user import router as user_router
from app.routers.vehiculo import router as vehiculo_router
from app.routers.ticket import router as ticket_router
from app.routers.factura import router as factura_router
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno desde el archivo .env
env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path)

# Crear tablas en la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

origins = [
    "http://localhost:5173"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(user_router)
app.include_router(vehiculo_router)
app.include_router(ticket_router)
app.include_router(factura_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
