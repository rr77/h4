# pages/5_ExportPDF.py

import streamlit as st
import pandas as pd
from utils.calculations import calcular_flujo
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Exportar PDF", layout="wide")
st.title("📤 Exportar Resultados a PDF")

if "parametros" not in st.session_state:
    st.error("❌ No hay parámetros cargados. Ve a la página '1_Inputs' para configurar un escenario.")
    st.stop()

params = st.session_state["parametros"]
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

# Crear PDF con FPDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, txt="Resumen de Simulación – Foodtruck Burger Co.", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", size=10)
pdf.cell(200, 10, txt="Parámetros de entrada:", ln=True)
for key, val in params.items():
    pdf.cell(200, 8, txt=f"{key.replace('_', ' ').capitalize()}: {val}", ln=True)

pdf.ln(10)
pdf.set_font("Arial", "B", 12)
pdf.cell(200, 10, txt="Flujo de Caja (Primeras 12 Semanas):", ln=True)

pdf.set_font("Arial", size=8)
subset = flujo.head(12).copy()
subset.reset_index(drop=True, inplace=True)

col_names = list(subset.columns)
pdf.cell(200, 6, txt=" | ".join(col_names), ln=True)
for i in range(len(subset)):
    row = subset.iloc[i].tolist()
    formatted = [f"{v:,.0f}" if isinstance(v, (int, float)) else str(v) for v in row]
    pdf.cell(200, 6, txt=" | ".join(formatted), ln=True)

# Guardar y mostrar botón de descarga
temp_dir = tempfile.mkdtemp()
pdf_path = os.path.join(temp_dir, "Simulacion_Foodtruck.pdf")
pdf.output(pdf_path)

with open(pdf_path, "rb") as f:
    st.download_button("📄 Descargar PDF", f, file_name="Simulacion_Foodtruck.pdf", mime="application/pdf")
