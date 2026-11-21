# Declaración de uso de inteligencia artificial

**Herramienta:** Claude (Anthropic), asistente de IA, usado el 20 de noviembre de 2026.

*La reflexión del equipo y la decisión final sobre recomendaciones corresponden al equipo.*

## Para qué se usó

| Tarea | Qué hizo la IA | Qué revisó o decidió el equipo |
|---|---|---|
| Búsqueda de fuentes | Localizó los reportes de Nvidia y ASML en SEC EDGAR, los comunicados de la SIA y notas de prensa sobre eventos de 2025-2026. | Confirmar que cada fuente es pertinente y que las fechas coinciden con lo citado. |
| Código (Process y Analyze) | Redactó los notebooks de descarga, limpieza, validación, estudio de eventos y gráficas en Python. | Correr el notebook, revisar las validaciones y entender cada paso. |
| Borradores de las 6 fases | Propuso el planteamiento del problema, los 5 porqués, las brechas, las preguntas, la interpretación de resultados y las recomendaciones con KPIs, con base en los datos. | Ajustar la redacción, validar la lógica y decidir la versión final. |
| App Streamlit (21-nov-2026) | Programó la app que recorre las 6 fases, la página de limpieza por base, el tablero y la pestaña "Modelo para decidir" (entrenamiento, validación, proyección y regla de decisión). | Revisar que el modelo y sus umbrales tengan sentido para el caso, y entender cómo se eligió el modelo y qué significa su error. |
| Bitácora | Documentó las decisiones de limpieza tomadas en el código. | Confirmar que reflejan los criterios del equipo. |

## Controles aplicados

- Todas las cifras del reporte provienen de los archivos de datos, no de la memoria del modelo.
- Las cifras clave se cotejaron contra el texto de los reportes oficiales (validación V6 del notebook).
- Los hechos posteriores a mediados de 2025 se verificaron con fuentes externas y con los propios reportes de Nvidia.
- Se señalan como pendientes los datos que no se pudieron verificar.
- No se ingresaron datos personales ni confidenciales en la herramienta.
- Las relaciones entre controles y crecimiento de rivales se presentan como asociación, no como causalidad.
