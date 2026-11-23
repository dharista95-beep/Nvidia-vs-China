# Nvidia y China: cómo manejar la dependencia de un mercado que se puede cerrar

Estudio de caso final de la materia Ciencia de Datos (Universidad Anáhuac Puebla), impartida por el Dr. Farid Krayem Pineda y la profesora Leslie Marjorie Gallegos Salazar. Analiza cómo los controles de exportación de chips de inteligencia artificial de EE.UU. hacia China (2022-2026) afectaron a Nvidia y a sus competidores chinos, siguiendo las seis fases del análisis de datos.

**Equipo:** Paul Carreto Pérez, Rosa Delia Hernández Arista, Fernando Torres Villalobos y Alejandro Victoria Castelán.

## Documento final

La versión final del caso está en `docs/Caso_Nvidia_China.pdf`: cuerpo, referencias APA y anexos A a J.

## Contenido del repositorio

| Carpeta o archivo | Qué contiene |
|---|---|
| `docs/Caso_Nvidia_China.pdf` | Documento final del caso. |
| `docs/bitacora_decisiones.md` | Bitácora de decisiones de limpieza (D-xx) y de análisis (A-xx). La app la muestra en la página de limpieza. |
| `docs/uso_de_ia.md` | Declaración de uso de inteligencia artificial. |
| `notebooks/01_prepare_process.ipynb` | Descarga, limpieza y validación de los datos (fases Preparar y Procesar). |
| `notebooks/02_analyze_share.ipynb` | Preguntas P1 a P4, modelo y figuras (fases Analizar y Compartir). |
| `app/` | Aplicación Streamlit con las seis fases, tablero de indicadores y modelo con escenarios ajustables. Instrucciones en `app/README.md`. |
| `data/raw/` | Datos tal como se extrajeron. |
| `data/clean/` | Tablas limpias (ver el diccionario de datos abajo). |
| `data/resultados/` | Tablas de resultados del análisis. |
| `figuras/` | Gráficas en PNG que usan el documento y la app. |

## Diccionario de datos (data/clean)

**nvda_ingresos_trimestrales.csv** (una fila por trimestre y base; montos en millones de USD)
- `anio_fiscal`, `trimestre`, `periodo` (ej. FY2026-Q2), `fin` (último día del trimestre). El año fiscal de Nvidia termina a fines de enero.
- `base`: `facturacion` (método anterior) o `sede_cliente` (método desde oct-2025). No mezclar.
- `total`, `data_center`, `gaming`, `eeuu`, `taiwan`, `china`, `otros`.
- `pct_china`, `pct_eeuu`, `pct_dc`: porcentaje del total.

**nvda_ingresos_trimestrales_largo.csv**: mismo contenido en formato largo, con `origen` (reportado o derivado) y el archivo de la SEC de donde salió cada dato.

**nvda_ingresos_anuales.csv**: totales anuales FY2019-FY2026 en ambas bases.

**precios_diarios_eeuu.csv**: `fecha`, precio ajustado de AMD, ASML, NVDA, SP500, SOX, y rendimientos logarítmicos `r_*`.

**precios_diarios_rivales_china.csv**: precios ajustados en CNY de Cambricon (688256.SS), Hygon (688041.SS) y SMIC (688981.SS).

**eventos_controles_exportacion.csv**: `id`, `fecha_anuncio`, `fecha_reaccion` (día en que el mercado pudo reaccionar), `origen` (EE.UU. o China), `descripcion`, `fuente`.

**rivales_china_ingresos_anuales.csv**: `empresa`, `anio`, `ingresos_millones`, `moneda`, `crec_anual_pct`.

**asml_ingresos_china_anual.csv**: `anio`, `china_meur`, `total_meur` (millones de euros), `pct_china`.

**semiconductores_ventas_globales_sia.csv**: `anio`, `ventas_globales_musd`, `crec_pct`, `fuente`.

## Para reproducir
```
pip install pandas lxml yfinance matplotlib requests
export SEC_USER_AGENT="Nombre del equipo correo@dominio"
cd notebooks && jupyter nbconvert --to notebook --execute 01_prepare_process.ipynb
jupyter nbconvert --to notebook --execute 02_analyze_share.ipynb
```
