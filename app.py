# app.py

import streamlit as st

st.set_page_config(
    page_title="Foodtruck Simulator",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Foodtruck Burger Simulator")

st.markdown("""
Bienvenido al simulador interactivo de tu hamburguesería tipo foodtruck en Miami.

Usa el menú de la izquierda para explorar las distintas secciones:

- ⚙️ *Configuración de escenarios*: Define parámetros como pedidos por día, ticket promedio, costos, etc.
- 💵 *Flujo de caja*: Visualiza ingresos, costos y punto de equilibrio.
- 📊 *Comparación de escenarios*: Revisa cómo cambian los resultados bajo distintos supuestos.
- 🎲 *Simulación de Monte Carlo*: Evalúa el riesgo y la probabilidad de éxito.
- 📄 *Exportación PDF*: Descarga un informe con resultados financieros y parámetros.

---
Desarrollado con ❤️ en Streamlit para decisiones informadas e inversores exigentes.
""")
