# pages/4_MonteCarlo.py

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from utils.calculations import calcular_flujo

st.set_page_config(page_title="Simulación Monte Carlo", layout="wide")
st.title("🎲 Simulación Monte Carlo – Riesgo y Probabilidad")

st.sidebar.header("🎛️ Parámetros de Simulación")
num_simulaciones = st.sidebar.slider("Número de simulaciones", 100, 2000, 1000, step=100)
semanas = st.sidebar.slider("Duración en semanas", 8, 52, 24)

st.sidebar.markdown("---")

# Definir distribuciones (con controles)
pedidos_media = st.sidebar.number_input("Media de pedidos/día", value=40)
pedidos_std = st.sidebar.number_input("Desviación estándar", value=8.0)

ticket_media = st.sidebar.number_input("Ticket promedio medio ($)", value=16.0)
ticket_std = st.sidebar.number_input("Desviación estándar del ticket", value=2.0)

costo_variable_media = st.sidebar.number_input("Costo variable medio ($)", value=6.0)
costo_variable_std = st.sidebar.number_input("Desviación estándar del costo variable", value=0.8)

# Constantes
capex = 55000
marketing_mensual = 600
costos_fijos_semanales = 1800

dias_por_semana = 6

resultados = []
breakeven_count = 0

for i in range(num_simulaciones):
    pedidos_sim = max(1, np.random.normal(pedidos_media, pedidos_std))
    ticket_sim = max(1.0, np.random.normal(ticket_media, ticket_std))
    costo_sim = max(1.0, np.random.normal(costo_variable_media, costo_variable_std))

    flujo = calcular_flujo(
        pedidos_por_dia=pedidos_sim,
        ticket_promedio=ticket_sim,
        dias_por_semana=dias_por_semana,
        costos_variables_por_orden=costo_sim,
        costos_fijos_semanales=costos_fijos_semanales,
        gasto_marketing_mensual=marketing_mensual,
        capex_inicial=capex,
        semanas=semanas
    )
    final_cash = flujo.iloc[-1]["Cash Flow Acumulado"]
    breakeven = (flujo["Cash Flow Acumulado"] > 0).any()
    if breakeven:
        breakeven_count += 1
    resultados.append(final_cash)

resultados_array = np.array(resultados)

st.subheader("📊 Distribución del Cash Flow Final (Semana {semanas})")
data = pd.DataFrame({"Cash Flow Final": resultados_array})

hist = alt.Chart(data).mark_bar().encode(
    alt.X("Cash Flow Final", bin=alt.Bin(maxbins=50)),
    y='count()'
).properties(width=800, height=400)

st.altair_chart(hist, use_container_width=True)

st.subheader("📋 Estadísticas")
st.metric("Media del Cash Flow Final", f"${resultados_array.mean():,.0f}")
st.metric("Mediana (P50)", f"${np.percentile(resultados_array, 50):,.0f}")
st.metric("P10 / P90", f"${np.percentile(resultados_array, 10):,.0f} / ${np.percentile(resultados_array, 90):,.0f}")
st.metric("Probabilidad de alcanzar Break-even", f"{(breakeven_count / num_simulaciones) * 100:.1f}%")
