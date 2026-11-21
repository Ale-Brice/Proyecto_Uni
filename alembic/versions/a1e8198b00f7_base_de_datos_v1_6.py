"""base de datos v1.6

Revision ID: a1e8198b00f7
Revises: e07a7702b0d1
Create Date: 2026-11-19 20:35:59.714530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1e8198b00f7'
down_revision: Union[str, Sequence[str], None] = 'e07a7702b0d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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

    op.execute("CREATE INDEX ix_audit_log_table_name ON audit_log (table_name);")

    op.execute("CREATE INDEX ix_audit_log_changed_by ON audit_log (changed_by);")

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
                -- Eliminar el trigger si ya existe para evitar el error
                EXECUTE format('DROP TRIGGER IF EXISTS audit_%I_trigger ON %I;', t, t);

                -- Crear el trigger nuevamente
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

    op.execute("DROP FUNCTION IF EXISTS audit_trigger_func();")

    op.execute("DROP TABLE IF EXISTS audit_log;")
