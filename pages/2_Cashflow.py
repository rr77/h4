# pages/2_Cashflow.py

import streamlit as st
from utils.calculations import calcular_flujo, calcular_punto_equilibrio
import pandas as pd

st.set_page_config(page_title="Flujo de Caja", layout="wide")
st.title("💵 Flujo de Caja Simulado")

if "parametros" not in st.session_state:
    st.error("❌ No se han definido parámetros. Ve a la página '1_Inputs' para configurar un escenario.")
    st.stop()

# Cargar parámetros desde sesión
params = st.session_state["parametros"]

# Calcular flujo
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

# Mostrar gráficos y tablas
st.subheader("📈 Evolución del Cash Flow Acumulado")
st.line_chart(flujo.set_index("Semana")["Cash Flow Acumulado"], height=400)

st.subheader("📋 Detalle de Flujo Semanal")
st.dataframe(flujo, use_container_width=True)

# Calcular y mostrar punto de equilibrio
semana_equilibrio = calcular_punto_equilibrio(flujo)
if semana_equilibrio:
    st.success(f"✅ Punto de equilibrio alcanzado en la semana {semana_equilibrio}.")
else:
    st.warning("⚠️ No se alcanza el punto de equilibrio en el período simulado.")
