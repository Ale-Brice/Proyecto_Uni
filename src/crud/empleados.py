from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import empleado
from sqlalchemy.future import select

async def registrar_empleado(db: AsyncSession, nombre: str, apellido: str, numero: str, email: str):
    new_empleado = empleado(nombre=nombre, apellido=apellido, numero=numero, email=email)
    db.add(new_empleado)
    await db.commit()
    await db.refresh(new_empleado)
    return new_empleado

async def obt_empleados(db: AsyncSession):
    query = select(empleado).where(empleado.is_active == True)
    result = await db.execute(query)
    empleados = result.scalars().all()
    return empleados

async def del_empleado(db: AsyncSession, id: int):
    emp = await db.get(empleado, id)

    if not emp:
        return emp

    emp.is_active = False
    await db.commit()
    await db.refresh(emp)
    return emp

async def up_empleado(db: AsyncSession, id: int, new_name: str, apellido: str, numero: str, email: str):
    emp = await db.get(empleado, id)

    if not emp:
        return None

    emp.nombre = new_name
    emp.apellido = apellido
    emp.numero = numero
    emp.email = email
    await db.commit()
    await db.refresh(emp)
    return emp