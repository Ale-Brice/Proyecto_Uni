from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from jinja2 import Template
from weasyprint import HTML
import datetime
from src.crud.gastos import obt_cost_adm_mes
from src.crud.gastos import obt_cost_op_mes
from src.crud.gastos import obt_materia_p_mes
from src.db.session import get_db
from src.db.base import cost_adm, cost_op, materia_p

# Importa tus dependencias y cruds
# from src.api.deps import get_db
# from src.crud import cost_adm, cost_op, materia_p

router = APIRouter()

@router.get("/reporte-mensual/{year}/{month}")
async def generar_reporte_mensual(year: int, month: int, db: AsyncSession = Depends(get_db)):

    admin_costs = await obt_cost_adm_mes(db, year, month)
    oper_costs = await obt_cost_op_mes(db, year, month)
    materias = await obt_materia_p_mes(db, year, month)


    total_adm = sum(c.gasto_administrativo for c in admin_costs)
    total_op = sum(c.gasto_operativo for c in oper_costs)

    # Para materia prima, el costo es precio * cantidad
    total_mat = sum((m.precio_mat * m.cantidad) for m in materias)

    gran_total = total_adm + total_op + total_mat

    # 3. Preparar la plantilla HTML (versión simplificada)
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Helvetica, sans-serif; color: #333; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border-bottom: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .total-row { font-weight: bold; background-color: #e9ecef; }
            .summary { font-size: 18px; margin-bottom: 30px; }
        </style>
    </head>
    <body>
        <h1>Reporte de Costos - {{ mes }}/{{ anio }}</h1>

        <div class="summary">
            <p><strong>Total Administrativo:</strong> ${{ total_adm }}</p>
            <p><strong>Total Operativo:</strong> ${{ total_op }}</p>
            <p><strong>Total Materia Prima:</strong> ${{ total_mat }}</p>
            <h2>Gran Total: ${{ gran_total }}</h2>
        </div>

        <h3>Gastos Administrativos</h3>
        <table>
            <tr><th>Fecha</th><th>Tipo</th><th>Monto</th></tr>
            {% for c in admin_costs %}
            <tr><td>{{ c.fecha }}</td><td>{{ c.tipo_costo }}</td><td>${{ c.gasto_administrativo }}</td></tr>
            {% endfor %}
        </table>

        <h3>Gastos Operativos</h3>
        <table>
            <tr><th>Fecha</th><th>Tipo</th><th>Monto</th></tr>
            {% for c in oper_costs %}
            <tr><td>{{ c.fecha }}</td><td>{{ c.tipo_gasto_operativo }}</td><td>${{ c.gasto_operativo }}</td></tr>
            {% endfor %}
        </table>

        <h3>Materia Prima</h3>
        <table>
            <tr><th>Fecha</th><th>Material</th><th>Cantidad</th><th>Precio Unit.</th><th>Total</th></tr>
            {% for m in materias %}
            <tr>
                <td>{{ m.fecha }}</td>
                <td>{{ m.tipo_material }}</td>
                <td>{{ m.cantidad }}</td>
                <td>${{ m.precio_mat }}</td>
                <td>${{ m.precio_mat * m.cantidad }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    # 4. Renderizar y convertir a PDF
    template = Template(html_template)
    html_content = template.render(
        mes=month, anio=year,
        admin_costs=admin_costs, oper_costs=oper_costs, materias=materias,
        total_adm=total_adm, total_op=total_op, total_mat=total_mat, gran_total=gran_total
    )

    pdf_bytes = HTML(string=html_content).write_pdf()

    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f'inline; filename="reporte_costos_{year}_{month}.pdf"'}
    )