from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import cliente
from sqlalchemy.future import select

async def registrar_cliente(db: AsyncSession, nombre: str, apellido: str, numero: str, email: str):
    new_cliente = cliente(nombre=nombre, apellido=apellido, numero=numero, email=email)
    db.add(new_cliente)
    await db.commit()
    await db.refresh(new_cliente)
    return new_cliente

async def obt_clientes(db: AsyncSession):
    query = select(cliente).where(cliente.is_active == True)
    result = await db.execute(query)
    clientes = result.scalars().all()
    return clientes

async def del_cliente(db: AsyncSession, id: int):
    cli = await db.get(cliente, id)

    if not cli:
        return cli

    cli.is_active = False
    await db.commit()
    await db.refresh(cli)
    return cli

async def up_cliente(db: AsyncSession, id: int, new_name: str, apellido: str, numero: str, email: str):
    cli = await db.get(cliente, id)

    if not cliente:
        return None

    cli.nombre = new_name
    cli.apellido = apellido
    cli.numero = numero
    cli.email = email
    await db.commit()
    await db.refresh(cli)
    return cli