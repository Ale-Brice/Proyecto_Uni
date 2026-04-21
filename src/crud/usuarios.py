from sqlalchemy.orm import Session
from src.models.usuarios import Usuario
from src.schemas.usuarios import InicioSesion

def obtener_usuario_por_nombre(db: Session, nombre: str):
    return db.query(Usuario).filter(Usuario.name == nombre).first()