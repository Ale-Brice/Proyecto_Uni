from sqlalchemy.orm import Session
from src.models.usuarios import Usuario
from schemas.val_login import InicioSesion

def obtener_usuario_por_nombre(db: Session, nombre: str, clave_proporcionada: str):
    usuario = db.query(Usuario).filter(Usuario.name == nombre).first()

    if not usuario:
        return None

    if usuario.contrasena != clave_proporcionada:
        return None
    return usuario