# App Streamlit del caso Nvidia-China

Recorre el estudio completo por fases, en lenguaje sencillo para un cliente no técnico.
Usa las tablas de `../data/` y las figuras de `../figuras/`; no descarga nada de internet.

## Cómo correrla en VS Code

1. Abrir la carpeta `nvidia_china/` completa en VS Code (la app lee `data/`, `docs/` y `figuras/`).
2. Abrir una terminal (Terminal > New Terminal) y ejecutar:

```
cd app
python -m venv .venv
# Windows:   .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

3. Se abre el navegador en http://localhost:8501. Para detenerla: `Ctrl + C` en la terminal.

## Páginas

| Página | Contenido |
|---|---|
| Inicio | Pregunta central, cifras clave y las 4 preguntas con título claro |
| 1. Preguntar | Problema, 5 porqués, brechas y preguntas |
| 2. Preparar | Qué trae cada base, de dónde viene, qué significa cada columna y evaluación ROCCC |
| 3. Limpiar | Por cada una de las 7 bases: revisión de calidad, repetidos, reglas de validación, decisiones con su razón, original vs. limpia y gráfica de la limpieza |
| 4. Analizar | Una pestaña por pregunta; cada gráfica con "¿Cómo se lee?" y "¿Qué nos dice?" |
| 4b. Modelo para decidir | Entrena 3 modelos simples con las ventas trimestrales, elige el mejor por su error en trimestres que no vio, proyecta el próximo año, lo combina con escenarios de China (sliders) y aplica una regla de decisión para el inversionista |
| 5. Compartir | Tablero (dashboard) con KPIs, filtros y 4 gráficas |
| 6. Actuar | Escenario actual, tablero de KPIs vs. meta y recomendaciones |
| Glosario | H20, H200, SOX, movimiento extra (CAR), etc., con buscador |

## Archivos

- `app.py`: menú y navegación.
- `textos.py`: todos los textos en lenguaje sencillo (glosario, bases, preguntas, recomendaciones). Para cambiar una redacción, se edita aquí.
- `estilos.py`: tarjetas, tablas y cajas de explicación.
- `analisis.py`: carga de datos y cálculos (mismas funciones que los notebooks).
- `paginas/`: una página por fase (`limpiar.py`, `analizar.py`, `modelo.py`, `tablero.py`, `otras.py`).
