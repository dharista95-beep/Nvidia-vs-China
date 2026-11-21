# Bitácora de decisiones (fases Prepare y Process)

Cada decisión tiene un identificador que también aparece en el notebook `notebooks/01_prepare_process.ipynb`.

| ID | Fecha | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|---|
| D-01 | 20-nov-2026 | Fecha de corte de los datos: 20-nov-2026. Último reporte de Nvidia: 10-Q del 2.º trimestre del año fiscal 2027 (cerrado el 26-jul-2026). | Reproducibilidad: cualquiera que corra el notebook obtiene los mismos precios. | Dejar la fecha abierta (los resultados cambiarían cada día). |
| D-02 | 20-nov-2026 | Usar los datos XBRL de los 10-K/10-Q desde el 3.er trimestre del año fiscal 2020. | XBRL es el formato oficial y legible por máquina; evita copiar tablas a mano. Cubre al menos 2 años antes del primer control (ago-2022). | Copiar tablas del PDF (propenso a errores). |
| D-03 | 20-nov-2026 | Usar sólo región (EE.UU., Taiwán, China), mercado (Data Center, Gaming) y total. | Responden directamente a P1 y P3; el resto no aporta a la pregunta. | Incluir todos los mercados (Automotriz, Visualización profesional), que son menores. |
| D-04 | 20-nov-2026 | Unir `country:CN` (FY2019-FY2022) con `ChinaIncludingHongKongMember` como una sola variable "china". | En FY2021-FY2022, que aparecen con ambas etiquetas, los valores son idénticos (3,886 y 7,111 MUSD). | Tratar como dos variables distintas. |
| D-05 | 20-nov-2026 | Mantener dos bases geográficas separadas: "facturacion" (hasta FY2026-T2) y "sede_cliente" (desde FY2025-T3, re-expresado). | Nvidia cambió la metodología en el 10-Q de oct-2025; con la base nueva China pesa más (ej. 19.2% vs. 13.1% en FY2025). Mezclarlas crearía un salto falso. | Empalmar las series en una sola. |
| D-06 | 20-nov-2026 | Si un mismo periodo y base aparece en varios reportes, usar el del reporte más reciente. | Los reportes posteriores incluyen correcciones. Se verificó que dentro de una misma base no hubo re-expresiones. | Usar el primer valor publicado. |
| D-07 | 20-nov-2026 | Calcular el 4.º trimestre como anual (10-K) menos acumulado de 9 meses (10-Q del 3.er trimestre), dentro de la misma base. | Nvidia no publica 10-Q del 4.º trimestre. Se validó que la suma de 4 trimestres es igual al anual reportado. | Dejar el 4.º trimestre vacío. |
| D-08 | 20-nov-2026 | "Otros países" = total − EE.UU. − Taiwán − China. | Las categorías residuales cambiaron de nombre (Europa, Otra Asia-Pacífico, Singapur, Otros). Se validó que nunca es negativo. | Mantener cada categoría con su nombre original. |
| D-09 | 20-nov-2026 | Usar el precio de cierre ajustado. | Nvidia hizo splits 4:1 (jul-2021) y 10:1 (jun-2024); sin ajuste aparecerían caídas falsas de 75% y 90%. Se validó que ningún rendimiento diario supera ±50%. | Precio de cierre sin ajustar. |
| D-10 | 20-nov-2026 | Benchmarks: S&P 500 (mercado) y SOX (semiconductores). | Permiten separar el efecto del evento del movimiento general del mercado y del sector. | Sólo S&P 500 (no aísla el factor sectorial). |
| D-11 | 20-nov-2026 | Precios de acciones chinas en un archivo separado. | Otro calendario de días hábiles y otra moneda. | Unir todo en una tabla (crearía faltantes artificiales). |
| D-12 | 20-nov-2026 | Rendimientos logarítmicos diarios; se eliminan días con algún precio faltante en EE.UU. (no hubo ninguno). | Estándar en estudios de eventos; los rendimientos log se suman en el tiempo. | Rendimientos simples. |
| D-13 | 20-nov-2026 | Fecha de evento = primer día en que el mercado pudo reaccionar (día siguiente si el anuncio fue después del cierre). Ventana de análisis sugerida (−1, +1). | Evita asignar el efecto al día equivocado; la ventana cubre la incertidumbre en la hora del anuncio. Se validó que todas las fechas son días hábiles. | Usar la fecha de publicación tal cual. |
| D-14 | 20-nov-2026 | Ingresos de rivales chinos desde `yfinance`; se cotejaron Cambricon 2023-2024 y SMIC 2024 con sus reportes. Se corrigió la moneda de SMIC (USD, no CNY). | Las bolsas chinas no son accesibles desde nuestro entorno; `yfinance` reproduce los estados publicados. | Omitir rivales (dejaría P4 sin evidencia). |
| D-15 | 20-nov-2026 | Ventas globales de semiconductores capturadas a mano de los comunicados anuales de la SIA. | La SIA no ofrece API; son sólo 7 cifras. | Datos mensuales de WSTS (requieren suscripción). |
| D-16 | 20-nov-2026 | ASML sólo con datos anuales (20-F). | Es un recuadro comparativo; los datos trimestrales están en comunicados de prensa no estructurados. | Capturar trimestres a mano. |
| D-17 | 20-nov-2026 | Huawei (Ascend) se describe de forma cualitativa. | No cotiza en bolsa y no desglosa ingresos de chips de IA. | Usar estimaciones de terceros sin metodología pública. |

## Validaciones automáticas (todas pasaron)

| Validación | Resultado |
|---|---|
| V1: las regiones no exceden el total (otros ≥ 0) | OK |
| V2: el 4.º trimestre derivado no es negativo | OK |
| V3: suma de 4 trimestres = total anual reportado | OK |
| V4: Data Center ≤ total | OK |
| V5: serie en base facturación completa (24 trimestres, FY2020-T3 a FY2026-T2) | OK |
| V6: cotejo contra el texto del 10-K FY2026 (China 19,677 MUSD; total 215,938 MUSD) | OK |
| Precios: sin faltantes; ningún rendimiento diario > ±50% | OK |
| Eventos: las 12 fechas de reacción son días hábiles | OK |

## Decisiones de análisis (fase Analyze, `notebooks/02_analyze_share.ipynb`)

| ID | Decisión | Por qué |
|---|---|---|
| A-01 | Comparar el peso de China por "regímenes" regulatorios (R0 a R3) según el trimestre fiscal en que entró en vigor cada regla, dentro de cada base. | Sólo hay 1 a 12 trimestres por régimen; promedios por régimen son más claros que una regresión con tan pocos datos. |
| A-02 | Estudio de eventos con modelo de mercado, ventana de estimación de −250 a −11 días hábiles y ventana del evento de −1 a +1. | Método estándar en finanzas; la ventana corta reduce la contaminación por otras noticias. |
| A-03 | Dos referencias: S&P 500 y SOX. | El SOX aísla el efecto sectorial, pero Nvidia pesa mucho dentro de él, así que se reportan ambos. |
| A-04 | Significancia con prueba t individual (|t| > 1.96). | Con 12 eventos no se justifica una prueba más compleja; se aclara que la evidencia es indicativa. |
| A-05 | Clasificar cada evento como "restricción" o "apertura". | Permite comparar la reacción a noticias negativas y positivas. El acuerdo del 15% (E8) se clasificó como apertura porque permitía vender el H20. |
| A-06 | Descomponer el cambio de ingresos por región en FY2022→FY2025 (facturación) y FY2025→FY2026 (sede del cliente). | El primer periodo cubre los controles de 2022-2023; el segundo, el año en que China cayó en términos absolutos. |
| A-07 | Para comparar con la SIA y con ASML, asignar el año fiscal de Nvidia al año calendario anterior. | El año fiscal termina a fines de enero, así que coincide en 11 de 12 meses con el año calendario anterior. |
| A-08 | Para rivales, usar índices (2022 = 100) y no calcular correlaciones. | Monedas distintas y sólo 4 años: una correlación no sería informativa. |
| A-09 | Pestaña "Modelo para decidir" de la app: pronosticar las ventas trimestrales totales con tres modelos simples (ingenuo, crecimiento promedio y tendencia lineal sobre el logaritmo) con ventanas de 4, 8 y 12 trimestres. Se elige el modelo con menor error promedio en 8 trimestres de validación (pronóstico de un trimestre a la vez, entrenando sólo con datos anteriores) y se reporta su error en los últimos 4 trimestres como prueba. Se reportan MAPE (criterio de elección, porque las ventas crecieron unas 30 veces y el error en % trata parejo a todos los trimestres), MAE y RMSE en MUSD; no se usa matriz de confusión porque es un modelo de regresión, no de clasificación. | Con 28 trimestres un modelo complejo se sobreajustaría; separar validación y prueba evita elegir el modelo con los mismos datos con que se mide. La proyección se combina con escenarios de China y una regla de decisión con umbrales propuestos por el equipo (10%, 30%, 60%, 50%); es una proyección, no un resultado comprobado ni causal. |
