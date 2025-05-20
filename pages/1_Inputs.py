# pages/1_Inputs.py

import streamlit as st
from utils.calculations import presets

st.set_page_config(page_title="Escenarios de Simulación", layout="wide")
st.title("⚙️ Parámetros del Modelo – Escenarios Editables")

preset_options = presets()

# Selección de escenario preconfigurado
escenario = st.selectbox("Selecciona un escenario base", list(preset_options.keys()))
parametros = preset_options[escenario].copy()

st.markdown("---")
st.subheader(f"✏️ Edita los parámetros de: {escenario}")

# Inputs agrupados
col1, col2, col3 = st.columns(3)

parametros["pedidos_por_dia"] = col1.number_input("Pedidos por día", value=parametros["pedidos_por_dia"], min_value=1)
parametros["ticket_promedio"] = col2.number_input("Ticket promedio ($)", value=parametros["ticket_promedio"], min_value=1.0)
parametros["dias_por_semana"] = col3.slider("Días de operación por semana", 1, 7, value=parametros["dias_por_semana"])

parametros["costos_variables_por_orden"] = col1.number_input("Costo variable por orden ($)", value=parametros["costos_variables_por_orden"], min_value=0.0)
parametros["costos_fijos_semanales"] = col2.number_input("Costos fijos semanales ($)", value=parametros["costos_fijos_semanales"], min_value=0.0)
parametros["gasto_marketing_mensual"] = col3.number_input("Gasto mensual en marketing ($)", value=parametros["gasto_marketing_mensual"], min_value=0.0)

parametros["capex_inicial"] = col1.number_input("CapEx inicial ($)", value=parametros["capex_inicial"], min_value=0.0)
parametros["semanas"] = col2.slider("Duración de simulación (semanas)", 4, 52, value=parametros["semanas"])

st.markdown("---")
st.success("✅ Parámetros cargados y listos para simular desde la página principal")

st.session_state["parametros"] = parametros
