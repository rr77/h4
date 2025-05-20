# utils/calculations.py

import pandas as pd

def presets():
    return {
        "Conservador": {
            "pedidos_por_dia": 20,
            "ticket_promedio": 14.0,
            "dias_por_semana": 5,
            "costos_variables_por_orden": 7.0,
            "costos_fijos_semanales": 1600.0,
            "gasto_marketing_mensual": 400.0,
            "capex_inicial": 60000.0,
            "semanas": 24
        },
        "Base": {
            "pedidos_por_dia": 40,
            "ticket_promedio": 16.0,
            "dias_por_semana": 6,
            "costos_variables_por_orden": 6.0,
            "costos_fijos_semanales": 1800.0,
            "gasto_marketing_mensual": 600.0,
            "capex_inicial": 55000.0,
            "semanas": 24
        },
        "Optimista": {
            "pedidos_por_dia": 60,
            "ticket_promedio": 18.0,
            "dias_por_semana": 6,
            "costos_variables_por_orden": 5.5,
            "costos_fijos_semanales": 2000.0,
            "gasto_marketing_mensual": 800.0,
            "capex_inicial": 50000.0,
            "semanas": 24
        }
    }

def calcular_flujo(
    pedidos_por_dia,
    ticket_promedio,
    dias_por_semana,
    costos_variables_por_orden,
    costos_fijos_semanales,
    gasto_marketing_mensual,
    capex_inicial,
    semanas
):
    ingresos_semanales = pedidos_por_dia * dias_por_semana * ticket_promedio
    costos_variables_semanales = pedidos_por_dia * dias_por_semana * costos_variables_por_orden
    margen_bruto_semanal = ingresos_semanales - costos_variables_semanales
    beneficio_neto_semanal = margen_bruto_semanal - costos_fijos_semanales - (gasto_marketing_mensual / 4)

    flujo = pd.DataFrame({
        "Semana": range(1, semanas + 1),
        "Ingresos": ingresos_semanales,
        "Costos Variables": costos_variables_semanales,
        "Costos Fijos": costos_fijos_semanales,
        "Marketing": gasto_marketing_mensual / 4,
        "Beneficio Neto": beneficio_neto_semanal,
    })
    flujo["Cash Flow Acumulado"] = flujo["Beneficio Neto"].cumsum() - capex_inicial

    return flujo

def calcular_punto_equilibrio(flujo):
    breakeven = flujo[flujo["Cash Flow Acumulado"] > 0]["Semana"].min()
    return int(breakeven) if not pd.isna(breakeven) else None
