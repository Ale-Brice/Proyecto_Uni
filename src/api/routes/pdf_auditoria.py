from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from jinja2 import Template
from weasyprint import HTML
from src.db.session import get_db
from src.crud.pdf_audit import obt_audit_log_mes
from zoneinfo import ZoneInfo

router = APIRouter()

# Plantilla HTML optimizada para auditoría (Diseño Horizontal / Landscape)
AUDIT_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        @page {
            size: A4 landscape;
            margin: 15mm 12mm;
            background-color: #f8fafc;
        }
        body {
            margin: 0; padding: 0;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #1e293b; font-size: 9.5pt; line-height: 1.4;
        }
        .header-banner {
            background-color: #0f172a; color: #ffffff;
            padding: 16px 20px; margin: -15mm -12mm 20px -12mm;
        }
        .header-table { width: 100%; border-collapse: collapse; }
        .company-title { font-size: 16pt; font-weight: bold; }
        h2 {
            font-size: 11pt; border-left: 4px solid #2563eb;
            padding-left: 8px; margin-top: 15px; page-break-after: avoid;
        }
        .data-table {
            width: 100%; border-collapse: collapse; background: #ffffff;
            border: 1px solid #e2e8f0; border-radius: 6px; font-size: 9pt;
        }
        .data-table th {
            background: #f1f5f9; color: #334155; padding: 8px 10px;
            border-bottom: 2px solid #cbd5e1; text-align: left;
        }
        .data-table td { padding: 8px 10px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }
        .data-table tr:nth-child(even) { background-color: #f8fafc; }

        /* Badges de colores para las acciones */
        .badge-insert { background-color: #d1fae5; color: #065f46; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 8pt; }
        .badge-update { background-color: #fef3c7; color: #92400e; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 8pt; }
        .badge-delete { background-color: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 8pt; }

        tr { page-break-inside: avoid; }
    </style>
</head>
<body>
    <div class="header-banner">
        <table class="header-table">
            <tr>
                <td>
                    <div class="company-title">Reporte de Auditoría del Sistema</div>
                    <div style="color: #94a3b8; font-size: 9pt;">Registro de Actividad y Trazabilidad</div>
                </td>
                <td style="text-align: right; color: #cbd5e1; font-size: 9pt;">
                    <div>Periodo: <strong>{{ month }}/{{ year }}</strong></div>
                    <div>Total Movimientos: <strong>{{ total_logs }}</strong></div>
                </td>
            </tr>
        </table>
    </div>

    <h2>Historial de Operaciones Registradas</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th width="5%">ID</th>
                <th width="20%">Fecha / Hora</th>
                <th width="20%">Tabla Afectada</th>
                <th width="15%">Acción</th>
                <th width="40%">Usuario Responsable</th>
            </tr>
        </thead>
        <tbody>
            {% for log in audit_logs %}
            <tr>
                <td>#{{ log.id }}</td>
                <td>{{ log.fecha_formateada }}</td>
                <td><strong>{{ log.table_name }}</strong></td>
                <td>
                    {% if log.action == 'INSERT' %}
                        <span class="badge-insert">INSERT</span>
                    {% elif log.action == 'UPDATE' %}
                        <span class="badge-update">UPDATE</span>
                    {% else %}
                        <span class="badge-delete">{{ log.action }}</span>
                    {% endif %}
                </td>
                <td>{{ log.changed_by or 'Sistema / Desconocido' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@router.get("/reporte-auditoria/{year}/{month}", response_class=Response)
async def generar_reporte_auditoria(year: int, month: int, db: AsyncSession = Depends(get_db)):
    audit_logs = await obt_audit_log_mes(db, year, month)
    # Zona horaria local (UTC-4)
    tz_local = ZoneInfo("America/Caracas")
    # Formatear cada registro antes de enviarlo a Jinja2
    logs_formateados = []
    for log in audit_logs:
        # Convertir de UTC a hora local y quitar microsegundos
        fecha_local = log.created_at.astimezone(tz_local).strftime("%Y-%m-%d %H:%M:%S")
        # Si prefieres formato día/mes/año con AM/PM, usa:
        # fecha_local = log.created_at.astimezone(tz_local).strftime("%d/%m/%Y %I:%M:%S %p")
        logs_formateados.append({
            "id": log.id,
            "fecha_formateada": fecha_local,
            "table_name": log.table_name,
            "action": log.action,
            "changed_by": log.changed_by
        })

    template = Template(AUDIT_HTML_TEMPLATE)
    html_rendered = template.render(
        year=year,
        month=month,
        audit_logs=logs_formateados,  # Pasamos la lista ya formateada
        total_logs=len(logs_formateados)
    )

    pdf_bytes = HTML(string=html_rendered).write_pdf()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={'Content-Disposition': f'inline; filename="reporte_auditoria_{year}_{month}.pdf"'}
    )