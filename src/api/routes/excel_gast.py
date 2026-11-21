from io import BytesIO
import pandas as pd
from fastapi import APIRouter, Depends, Response
from src.core.checker import PermissionChecker
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.audit import get_audited_db
from src.crud.gastos import obt_cost_adm_mes, obt_cost_op_mes, obt_materia_p_mes
from src.crud.ventas import obt_ventas_mes

require_view = PermissionChecker(["view"])

router = APIRouter()

@router.get("/reporte-mensual-excel/{year}/{month}")
async def generar_reporte_excel(year: int, month: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    admin_costs = await obt_cost_adm_mes(db, year, month)
    oper_costs = await obt_cost_op_mes(db, year, month)
    materias = await obt_materia_p_mes(db, year, month)
    ventas_mes = await obt_ventas_mes(db, year, month)

    total_adm = float(sum(c.gasto_administrativo for c in admin_costs))
    total_op = float(sum(c.gasto_operativo for c in oper_costs))
    total_mat = float(sum((m.precio_mat * m.cantidad) for m in materias))
    total_ingresos = float(sum((v.precio_p * v.cantidad) for v in ventas_mes))

    gran_total_gastos = total_adm + total_op + total_mat
    ganancia_neta = total_ingresos - gran_total_gastos

    df_resumen = pd.DataFrame([
        {"Concepto": "Total Ingresos (Ventas)", "Monto ($)": total_ingresos},
        {"Concepto": "Gastos Administrativos", "Monto ($)": total_adm},
        {"Concepto": "Gastos Operativos", "Monto ($)": total_op},
        {"Concepto": "Costo de Materia Prima", "Monto ($)": total_mat},
        {"Concepto": "TOTAL GASTOS", "Monto ($)": gran_total_gastos},
        {"Concepto": "GANANCIA NETA", "Monto ($)": ganancia_neta},
    ])

    df_adm = pd.DataFrame([
        {
            "Fecha": c.fecha,
            "Tipo de Costo": c.tipo_costo,
            "Monto ($)": float(c.gasto_administrativo)
        } for c in admin_costs
    ])

    df_op = pd.DataFrame([
        {
            "Fecha": c.fecha,
            "Tipo de Gasto": c.tipo_gasto_operativo,
            "Monto ($)": float(c.gasto_operativo)
        } for c in oper_costs
    ])

    df_mat = pd.DataFrame([
        {
            "Fecha": m.fecha,
            "Material": m.tipo_material,
            "Cantidad": m.cantidad,
            "Precio Unitario ($)": float(m.precio_mat),
            "Subtotal ($)": float(m.precio_mat * m.cantidad)
        } for m in materias
    ])

    df_ventas = pd.DataFrame([
        {
            "Fecha": v.fecha,
            "ID Producto": v.fk_producto,
            "Cantidad": v.cantidad,
            "Precio Unitario ($)": float(v.precio_p),
            "Subtotal ($)": float(v.precio_p * v.cantidad)
        } for v in ventas_mes
    ])

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_resumen.to_excel(writer, sheet_name="Resumen Financiero", index=False)
        
        # Validamos si hay datos para evitar hojas completamente vacías sin encabezados
        if not df_adm.empty:
            df_adm.to_excel(writer, sheet_name="Gastos Administrativos", index=False)
        if not df_op.empty:
            df_op.to_excel(writer, sheet_name="Gastos Operativos", index=False)
        if not df_mat.empty:
            df_mat.to_excel(writer, sheet_name="Materia Prima", index=False)
        if not df_ventas.empty:
            df_ventas.to_excel(writer, sheet_name="Ventas", index=False)

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for col in worksheet.columns:
                max_length = 0
                column_letter = col[0].column_letter
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                worksheet.column_dimensions[column_letter].width = max_length + 4

    buffer.seek(0)

    headers = {
        "Content-Disposition": f'attachment; filename="reporte_financiero_{year}_{month}.xlsx"'
    }
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )