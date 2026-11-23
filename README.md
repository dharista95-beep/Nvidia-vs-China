# Caso Nvidia-China: datos y documentación (Ask, Prepare, Process)

## Estructura y reparto sugerido del documento

El índice completo del PDF, con páginas por sección y qué va a anexos, está en `docs/estructura_documento_final.md`.

| Integrante | Secciones | Archivo |
|---|---|---|
| 1 | Resumen ejecutivo, Ask, narración del caso, conclusiones | `docs/00_resumen_ejecutivo_y_conclusiones.md`, `docs/01_ask.md`, `docs/03a_narracion_del_caso.md` |
| 2 | Prepare y Process | `docs/02_prepare_process.md`, `docs/bitacora_decisiones.md`, `notebooks/01_prepare_process.ipynb` |
| 3 | Analyze | `docs/03_analyze.md`, `notebooks/02_analyze_share.ipynb` |
| 4 | Share y Act | `docs/04_share_act.md`, `figuras/fig1` a `fig5` |
| Todos | Referencias, uso de IA, reflexión del equipo | `docs/referencias_apa.md`, `docs/uso_de_ia.md` |

Otras carpetas: `data/raw/` (datos tal como se extrajeron), `data/clean/` (tablas limpias), `data/resultados/` (tablas de resultados del análisis), `figuras/` (gráficas PNG listas para el PDF).

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
