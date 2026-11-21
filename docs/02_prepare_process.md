# FASE 2. PREPARE (Preparar)

> Sección autocontenida. Cifras de los reportes de Nvidia ante la SEC, procesadas en `notebooks/01_prepare_process.ipynb`. Fecha de corte de los datos: 20 de noviembre de 2026. Las referencias completas están en `docs/referencias_apa.md`.



## 2.1 Datos recopilados

| # | Conjunto de datos | Fuente | Periodo | Granularidad | Archivo limpio |
|---|---|---|---|---|---|
| 1 | Ingresos de Nvidia por región y por mercado | SEC EDGAR, XBRL de 10-K y 10-Q | FY2019 (anual) y FY2020-T3 a FY2027-T2 | Trimestral y anual | `nvda_ingresos_trimestrales.csv`, `nvda_ingresos_anuales.csv` |
| 2 | Precios diarios ajustados de NVDA, AMD, ASML, S&P 500, SOX | Yahoo Finance (`yfinance`) | 2-ene-2019 a 19-nov-2026 | Diaria | `precios_diarios_eeuu.csv` |
| 3 | Precios de Cambricon, Hygon y SMIC (Shanghái) | Yahoo Finance | 2019 a 2026 | Diaria | `precios_diarios_rivales_china.csv` |
| 4 | Ingresos anuales de Cambricon, Hygon y SMIC | Yahoo Finance (estados financieros) | 2022 a 2025 | Anual | `rivales_china_ingresos_anuales.csv` |
| 5 | Ingresos de ASML por región | SEC EDGAR, XBRL de 20-F | 2017 a 2025 | Anual | `asml_ingresos_china_anual.csv` |
| 6 | Ventas globales de semiconductores | SIA (datos WSTS) | 2019 a 2025 | Anual | `semiconductores_ventas_globales_sia.csv` |
| 7 | Calendario de eventos regulatorios | Reportes de Nvidia, BIS y prensa | 2022 a 2026 | Por evento | `eventos_controles_exportacion.csv` |

## 2.2 Evaluación de calidad (criterio ROCCC)

| Fuente | Confiable | Original | Completa | Actual | Citada | Comentario |
|---|---|---|---|---|---|---|
| SEC EDGAR (Nvidia, ASML) | Alta: reportes auditados y obligatorios | Sí, fuente primaria | Alta, con un quiebre metodológico en 2025 | Hasta jul-2026 | Sí | La mejor fuente disponible. Limitación: la región es la del cliente directo, no la del usuario final. |
| Yahoo Finance (precios) | Alta para precios de cierre | Secundaria (agrega datos de bolsa) | Completa en EE.UU. | Al 19-nov-2026 | Sí | Se usa el cierre ajustado por splits y dividendos. |
| Yahoo Finance (estados de rivales) | Media | Secundaria | Sólo 4 años | 2025 | Parcial | Se cotejó con reportes anuales; se detectó y corrigió un error de moneda (SMIC). |
| SIA / WSTS | Alta: referencia estándar de la industria | Primaria para la industria | Anual | 2025 | Sí | Capturada a mano desde comunicados de prensa. |
| Prensa (eventos 2025-2026) | Media-alta (Bloomberg, Reuters, FT) | Secundaria | Por evento | Sí | Sí | Las fechas se cruzan con lo que Nvidia reporta a la SEC cuando es posible. |

**Pertinencia:** cada fuente responde a una pregunta: SEC → P1 y P3; precios y eventos → P2; rivales y SIA → P4 y contexto; ASML → recuadro comparativo.

## 2.3 Limitaciones y sesgos conocidos

1. **Cambio de metodología (oct-2025).** Nvidia pasó de reportar por lugar de facturación a reportar por sede del cliente, y re-expresó sólo algunos periodos. Con la base nueva, China pesa más (por ejemplo, 19.2% vs. 13.1% en el año fiscal 2025). Se conservan ambas series, marcadas.
2. **Destino final desconocido.** Nvidia aclara que el lugar de envío y el cliente final pueden ser distintos a la sede o a la facturación. Ventas a través de terceros países (por ejemplo, Singapur) o contrabando no se ven en los datos.
3. **Huawei no cotiza** y no desglosa los ingresos de sus chips Ascend, así que sólo se describe cualitativamente.
4. **Rivales en yuanes, Nvidia en dólares**: se comparan tasas de crecimiento, no montos.
5. **Asociación no es causalidad:** que los rivales crezcan cuando se endurecen los controles no prueba que los controles lo causen (también influyen subsidios, demanda de IA y otras políticas).
6. **Datos confidenciales:** sólo se usan datos públicos; no hay información personal ni confidencial.

## 2.4 Hechos recientes verificados (después de mediados de 2025)

| Fecha | Hecho | Fuente |
|---|---|---|
| Abr-2025 | EE.UU. exige licencia para el H20; Nvidia registra un cargo de 4,500 MUSD (estimaba 5,500). | Nvidia (2026a) |
| Ago-2025 | EE.UU. otorga licencias para algunos H20; funcionarios esperan recibir 15% o más de esas ventas, pero nunca se publicó una regulación. Nvidia generó sólo ~60 MUSD en ventas de H20 con esas licencias. | Nvidia (2026a) |
| Sep-2025 | La agencia del ciberespacio de China (CAC) pide a grandes empresas dejar de comprar chips de Nvidia. | Bloomberg (2025) |
| Dic-2025 | Trump anuncia que se permitirá exportar el H200 a China con 25% para el gobierno de EE.UU. | Semafor (2025) |
| Ene-2026 | Aduanas chinas reciben instrucción de no permitir la entrada del H200. | Business Day (2026) |
| Feb-2026 | EE.UU. otorga a Nvidia licencia para enviar pequeñas cantidades de H200 a clientes chinos específicos; los chips pasan inspección en EE.UU. y pagan arancel de 25%. | Nvidia (2026a) |
| Ago-2026 | China permite entregas limitadas de H200 caso por caso (ByteDance, Tencent). | Business Standard (2026) |
| Jul-2026 | Las ventas de H200 a China son menos del 1% de los ingresos de Data Center; cargo de 400 MUSD por inventario de H200. | Nvidia (2026b) |

---

# FASE 3. PROCESS (Procesar)

## 3.1 Herramientas
Python 3.13 en Jupyter Notebook, con `pandas` (manejo de tablas), `lxml` (lectura de XBRL), `requests` (descarga de la SEC), `yfinance` (precios) y `matplotlib` (gráficas). Se eligió Python en lugar de hojas de cálculo porque son más de 2,000 días de precios y 31 reportes con más de 1,100 datos de ingresos, y porque el proceso debe poder repetirse.

## 3.2 Pasos de limpieza y transformación
1. **Extracción:** se descargaron los archivos XBRL (formato oficial y legible por máquina) de 24 reportes de Nvidia y 7 de ASML, y se extrajeron 1,122 datos de ingresos con sus dimensiones (región, mercado).
2. **Filtrado:** se conservaron sólo total, EE.UU., Taiwán, China (incl. Hong Kong), Data Center y Gaming (D-03).
3. **Homologación:** se unieron dos etiquetas de China que cambiaron con los años (D-04) y se calculó "otros países" como residuo (D-08).
4. **Separación por metodología:** cada dato geográfico se marcó como base "facturación" o "sede del cliente" según el reporte del que provino (D-05). Cuando un dato se repetía en varios reportes, se tomó el más reciente (D-06).
5. **Cálculo del 4.º trimestre:** anual menos acumulado de 9 meses (D-07).
6. **Precios:** cierre ajustado por splits (D-09), rendimientos logarítmicos diarios (D-12) y archivo separado para acciones chinas (D-11).
7. **Eventos:** se fijó el día en que el mercado pudo reaccionar a cada anuncio (D-13).
8. **Rivales:** se corrigió un error de moneda en SMIC detectado al cotejar con su reporte anual (D-14).

## 3.3 Validaciones (todas pasaron)

| Validación | Qué comprueba |
|---|---|
| V1 | Las regiones nunca suman más que el total |
| V2 | El 4.º trimestre calculado nunca es negativo |
| V3 | La suma de los 4 trimestres es igual al total anual reportado |
| V4 | Data Center nunca es mayor que el total |
| V5 | No faltan trimestres en la serie (24 en base facturación) |
| V6 | Cotejo contra el texto del 10-K FY2026: China 19,677 MUSD y total 215,938 MUSD |
| Precios | Sin faltantes y ningún rendimiento diario mayor a ±50% (descarta splits mal ajustados) |
| Eventos | Las 12 fechas de reacción son días hábiles |

## 3.4 Resultado
Nueve tablas limpias en `data/clean/` (descritas en el `README.md`), la bitácora de decisiones (`docs/bitacora_decisiones.md`) y la declaración de uso de IA (`docs/uso_de_ia.md`).
