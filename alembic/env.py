from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv
from src.db.base_class import Base
from src.models.usuarios import Usuario
from src.models.empleado import empleado
from src.models.pedido import pedido
from src.models.materia_p import materia_p
from src.models.producto import producto
from src.models.cliente import cliente
from src.models.detalle_pro import detalle_pro
from src.models.cost_op import cost_op, cost_adm


load_dotenv()
config = context.config
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
