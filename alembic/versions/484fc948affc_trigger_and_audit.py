"""Trigger and audit

Revision ID: 484fc948affc
Revises: f54bc66aa890
Create Date: 2026-08-01 22:15:50.404400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '484fc948affc'
down_revision: Union[str, Sequence[str], None] = 'f54bc66aa890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
# Sentencia 1: Crear la tabla
    op.execute("""
        CREATE TABLE audit_log (
            id SERIAL PRIMARY KEY,
            table_name VARCHAR(50) NOT NULL,
            action VARCHAR(10) NOT NULL,
            old_data JSONB,
            new_data JSONB,
            changed_by VARCHAR(100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
    """)

    # Sentencia 2: Primer índice
    op.execute("CREATE INDEX ix_audit_log_table_name ON audit_log (table_name);")

    # Sentencia 3: Segundo índice
    op.execute("CREATE INDEX ix_audit_log_changed_by ON audit_log (changed_by);")

    # Sentencia 4: La función del trigger (cuenta como 1 sentencia)
    op.execute("""
        CREATE OR REPLACE FUNCTION audit_trigger_func()
        RETURNS TRIGGER AS $$
        DECLARE
            user_id TEXT;
        BEGIN
            user_id := NULLIF(current_setting('app.current_user_id', true), '');

            IF (TG_OP = 'DELETE') THEN
                INSERT INTO audit_log (table_name, action, old_data, changed_by)
                VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(OLD), user_id);
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO audit_log (table_name, action, old_data, new_data, changed_by)
                VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(OLD), to_jsonb(NEW), user_id);
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO audit_log (table_name, action, new_data, changed_by)
                VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(NEW), user_id);
                RETURN NEW;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Sentencia 5: El bloque DO $$ que recorre todas las tablas (cuenta como 1 sentencia)
    op.execute("""
        DO $$
        DECLARE
            t text;
        BEGIN
            FOR t IN
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                  AND table_type = 'BASE TABLE'
                  AND table_name NOT IN ('audit_log', 'alembic_version')
            LOOP
                EXECUTE format('
                    CREATE TRIGGER audit_%I_trigger
                    AFTER INSERT OR UPDATE OR DELETE ON %I
                    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
                ', t, t);
            END LOOP;
        END;
        $$;
    """)


def downgrade() -> None:
# 1. Eliminar todos los triggers de auditoría dinámicamente
    op.execute("""
        DO $$
        DECLARE
            t text;
        BEGIN
            FOR t IN
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                  AND table_type = 'BASE TABLE'
                  AND table_name NOT IN ('audit_log', 'alembic_version')
            LOOP
                EXECUTE format('DROP TRIGGER IF EXISTS audit_%I_trigger ON %I;', t, t);
            END LOOP;
        END;
        $$;
    """)

    # 2. Eliminar función
    op.execute("DROP FUNCTION IF EXISTS audit_trigger_func();")

    # 3. Eliminar tabla audit_log
    op.execute("DROP TABLE IF EXISTS audit_log;")
