"""App del caso Nvidia-China: recorre las 6 fases del estudio.

Ejecutar desde esta carpeta:   streamlit run app.py
"""
import streamlit as st

import analisis as A
import estilos as E
import textos as T
from paginas import analizar, limpiar, modelo, otras, tablero

st.set_page_config(page_title="Nvidia y China", page_icon="📊", layout="wide")
E.iniciar()


@st.cache_data
def datos():
    return A.cargar()


@st.cache_data
def datos_raw():
    return A.cargar_raw()


PAGINAS = {
    "🏠 Inicio": lambda: otras.inicio(datos()),
    "1. Preguntar (Ask)": lambda: otras.ask(datos()),
    "2. Preparar (Prepare)": lambda: otras.prepare(datos()),
    "3. Limpiar (Process)": lambda: limpiar.render(datos(), datos_raw()),
    "4. Analizar (Analyze)": lambda: analizar.render(datos()),
    "4b. Modelo para decidir": lambda: modelo.render(datos()),
    "5. Compartir: tablero (Share)": lambda: tablero.render(datos()),
    "6. Actuar (Act)": lambda: otras.act(datos()),
    "📖 Glosario": lambda: otras.glosario(datos()),
}

st.sidebar.title("Nvidia y China")
st.sidebar.caption("Estudio de caso por fases")
pagina = st.sidebar.radio("Ir a", list(PAGINAS))

with st.sidebar.expander("🔎 ¿Qué significa…?"):
    termino = st.selectbox("Término", list(T.GLOSARIO), index=None, placeholder="Elige un término")
    if termino:
        st.write(T.GLOSARIO[termino])

st.sidebar.info("Recuerda: que dos cosas pasen al mismo tiempo no prueba que una cause la otra. "
                "Las recomendaciones tienen un efecto esperado, no comprobado. Ejercicio académico, no asesoría de inversión.")
st.sidebar.caption("Datos públicos con corte al 20-nov-2026. La app usa los archivos de `data/` y no descarga nada.")

PAGINAS[pagina]()
