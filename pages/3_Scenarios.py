# pages/3_Scenarios.py

import streamlit as st
import pandas as pd
import altair as alt
from utils.calculations import calcular_flujo, presets

st.set_page_config(page_title="Comparación de Escenarios", layout="wide")
st.title("📊 Comparación de Escenarios: Conservador vs Base vs Optimista")

escenarios = presets()
resultados = []

for nombre, params in escenarios.items():
    flujo = calcular_flujo(
        pedidos_por_dia=params["pedidos_por_dia"],
        ticket_promedio=params["ticket_promedio"],
        dias_por_semana=params["dias_por_semana"],
        costos_variables_por_orden=params["costos_variables_por_orden"],
        costos_fijos_semanales=params["costos_fijos_semanales"],
        gasto_marketing_mensual=params["gasto_marketing_mensual"],
        capex_inicial=params["capex_inicial"],
        semanas=params["semanas"]
    )
    flujo["Escenario"] = nombre
    resultados.append(flujo)

comparativo = pd.concat(resultados, ignore_index=True)

# Gráfico comparativo del cash flow acumulado
st.subheader("📈 Cash Flow Acumulado por Escenario")
chart = alt.Chart(comparativo).mark_line().encode(
    x="Semana",
    y="Cash Flow Acumulado",
    color="Escenario"
).properties(
    width=900,
    height=400
)
st.altair_chart(chart, use_container_width=True)

# Tabla resumen última semana
st.subheader("📋 Resumen al Final del Período")
resumen_final = comparativo.groupby("Escenario").tail(1)[[
    "Escenario", "Ingresos", "Costos Variables", "Costos Fijos", "Marketing", "Beneficio Neto", "Cash Flow Acumulado"
]].reset_index(drop=True)

st.dataframe(resumen_final, use_container_width=True)
