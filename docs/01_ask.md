# FASE 1. ASK (Preguntar)

> Sección autocontenida. Cifras de los reportes de Nvidia ante la SEC, procesadas en `notebooks/01_prepare_process.ipynb`. Fecha de corte de los datos: 20 de noviembre de 2026. Las referencias completas están en `docs/referencias_apa.md`.



## 1.1 Contexto del negocio

Nvidia Corporation es una empresa estadounidense que diseña unidades de procesamiento gráfico (GPU). Su negocio principal hoy son los chips para centros de datos (*Data Center*), que se usan para entrenar y ejecutar modelos de inteligencia artificial. Nvidia no fabrica: diseña y subcontrata la producción (principalmente a TSMC en Taiwán). Su plataforma de software CUDA genera altos costos de cambio para los clientes.

Desde 2022, el gobierno de EE.UU. ha restringido la exportación de chips de IA avanzados a China, y desde 2025 el gobierno chino también ha desalentado o bloqueado la compra de chips de Nvidia. En el mismo periodo, los ingresos totales de Nvidia crecieron de 26,974 millones de dólares (MUSD) en el año fiscal 2023 a 215,938 MUSD en el año fiscal 2026.

## 1.2 Planteamiento del problema

El peso de China (incluido Hong Kong) en los ingresos de Nvidia pasó de **26.4% en el año fiscal 2022** a **9.1% en el año fiscal 2026**, y tocó un mínimo de **4.5% en el 4.º trimestre del año fiscal 2026** (Nvidia, 2022, 2026a). Cada nueva regla obligó a Nvidia a diseñar versiones "recortadas" de sus chips (A800, H800, H20) que después también fueron restringidas, y generó cargos por inventario: 4,500 MUSD por el H20 en el 1.er trimestre del año fiscal 2026 y 400 MUSD por el H200 en el 1.er semestre del año fiscal 2027 (Nvidia, 2026a, 2026b).

**Problema:** Nvidia y sus inversionistas tienen una exposición importante a un mercado cuyo acceso depende de decisiones súbitas de dos gobiernos, y no cuentan con una forma sistemática de medir esa exposición ni de decidir cuánto riesgo aceptar.

**Pregunta central:** ¿Cómo debe Nvidia, o un inversionista, gestionar su exposición al mercado chino ante los controles de exportación de EE.UU.?

**Partes interesadas:**
- Dirección de Nvidia (estrategia comercial, inventario, diseño de producto).
- Inversionistas y analistas (valuación, riesgo de cartera).
- Clientes chinos de nube e IA, y competidores chinos (Huawei, Cambricon, Hygon, SMIC).
- Gobiernos de EE.UU. y China (reguladores, fuera del control de la empresa).

**Objetivo SMART:** Con datos públicos de los años fiscales 2020 a 2027 (2.º trimestre), cuantificar antes del 23 de noviembre de 2026 cuánto cambió el peso de China en los ingresos de Nvidia después de cada ronda de controles, cómo reaccionó la acción en los días de anuncio, y proponer al menos tres acciones con KPIs para gestionar esa exposición.

## 1.3 Propósito y justificación del estudio de caso

**Para qué:** extraer lecciones sobre cómo una empresa tecnológica, y quien invierte en ella, puede gestionar el acceso a un mercado grande cuando ese acceso depende de decisiones políticas. Los destinatarios son la dirección de estrategia de Nvidia y los inversionistas; el caso también sirve a otras empresas expuestas a controles de exportación (por ejemplo, ASML, AMD o fabricantes de equipo).

**Por qué vale la pena estudiarlo:** es uno de los pocos casos en que una política comercial afecta directamente a la empresa más valiosa de su industria, con datos públicos, trimestrales y auditados que permiten seguir el efecto en el tiempo. Además, las reglas siguen cambiando (2025-2026), así que las lecciones son útiles hoy.

**Hipótesis de trabajo:** Nvidia actuó bajo el supuesto de que podía conservar el mercado chino diseñando versiones de sus chips que cumplieran cada nueva regla (A800/H800, luego H20, luego H200). Este estudio examina si ese supuesto se sostuvo y qué costos tuvo.

## 1.4 Los 5 porqués

| # | Pregunta | Respuesta (con evidencia) |
|---|---|---|
| 1 | ¿Por qué cayó el peso de China en los ingresos de Nvidia? | Porque EE.UU. exigió licencias para exportar sus chips más avanzados a China: A100/H100 en 2022, A800/H800 en octubre de 2023 y H20 en abril de 2025 (Nvidia, 2026a). |
| 2 | ¿Por qué esas reglas pegaron tanto? | Porque el negocio de Nvidia se concentró en Data Center (89.7% de los ingresos en el año fiscal 2026), justo la categoría restringida, y China era uno de sus mayores mercados de nube e IA. |
| 3 | ¿Por qué los chips "recortados" para China no resolvieron el problema? | Porque los umbrales técnicos de las reglas se actualizan cada vez que aparece un producto adaptado, y desde 2025 el gobierno chino también pidió a sus empresas no comprar chips de Nvidia y frenó en aduana el H200 (Bloomberg, 2025; Business Day, 2026). |
| 4 | ¿Por qué China frena la compra si sus empresas los necesitan? | Por su política de autosuficiencia tecnológica y por el riesgo de depender de un proveedor sujeto a decisiones de EE.UU.; en el mismo periodo los ingresos de rivales locales crecieron (Cambricon pasó de 709 a 6,497 millones de yuanes entre 2023 y 2025). *Esto es una asociación en el tiempo, no prueba de causalidad.* |
| 5 | ¿Por qué esto es un problema de gestión y no sólo de ventas? | Porque ni Nvidia ni el inversionista controlan la regulación: el acceso a China puede abrirse o cerrarse en un día. Lo que sí se puede controlar es cuánto depende el negocio (o la cartera) de ese mercado y qué tan preparado está para cada escenario. |

**Causa raíz:** dependencia de ingresos de un mercado cuyo acceso decide la política de dos gobiernos, sin un mecanismo explícito para medir, limitar y cubrir esa exposición.

## 1.5 Análisis de brechas

| Dimensión | Estado actual | Estado deseado | Brecha | Cómo se medirá |
|---|---|---|---|---|
| Visibilidad de la exposición | Nvidia cambió en 2025 la forma de reportar regiones (de lugar de facturación a sede del cliente); las cifras no son comparables entre sí y el destino final del chip no se publica. | Una métrica estable y comparable de "ingresos expuestos a China" a lo largo del tiempo. | Falta una serie homogénea y una definición clara. | Peso de China en ingresos por trimestre, en ambas bases, marcando el cambio. |
| Dependencia de un mercado | China pasó de ~26% a ~5-9% de los ingresos, pero no por una decisión de Nvidia sino por la regulación. | Un nivel de exposición elegido conscientemente (por ejemplo, un tope) y no impuesto por eventos. | No existe un umbral explícito de tolerancia. | Peso de China vs. un tope propuesto; ingresos de otras regiones. |
| Respuesta del mercado bursátil | La acción reacciona a anuncios regulatorios de ambos países. | El inversionista conoce de antemano el tamaño típico de la reacción. | No hay estimación sistemática del impacto por evento. | Rendimientos anormales acumulados (estudio de eventos) vs. S&P 500 y SOX. |
| Costos por productos varados | Cargos por inventario: 4,500 MUSD (H20) y 400 MUSD (H200). | Producción de chips para China ligada a licencias ya aprobadas. | Se produce antes de tener certeza regulatoria. | Cargos por inventario relacionados con China como % de ingresos. |
| Competencia local | Rivales chinos crecen mientras Nvidia sale del mercado. | Monitoreo de la sustitución para anticipar pérdida permanente de mercado. | No se da seguimiento sistemático a rivales. | Crecimiento anual de ingresos de Cambricon, Hygon y SMIC. |

## 1.6 Pregunta de reflexión y preguntas de investigación

**Pregunta de reflexión (explicativa):** ¿Por qué la estrategia de Nvidia de adaptar sus chips a cada regla no logró sostener su posición en China, y qué factores explican que, aun así, su negocio total no se viera afectado de forma importante?

Para responderla, se plantean cuatro preguntas de investigación con datos:

1. **P1.** ¿Cuánto cambió el peso de China en los ingresos de Nvidia antes y después de cada ronda de controles (agosto/octubre 2022, octubre 2023, abril 2025) y tras la apertura parcial del H200 (diciembre 2025 a agosto 2026)?
2. **P2.** ¿Cómo reaccionó la acción de Nvidia, frente al S&P 500 y al índice de semiconductores SOX, en los días alrededor de los anuncios regulatorios de EE.UU. y de China?
3. **P3.** ¿En qué medida el crecimiento de Data Center y de otras regiones (EE.UU., Taiwán) compensó la pérdida de ingresos en China?
4. **P4.** ¿Los ingresos de los rivales chinos (Cambricon, Hygon, SMIC) crecieron en los mismos periodos en que se endurecieron los controles? *(Se interpretará como asociación, no como causalidad.)*

**Recuadro comparativo:** ASML, el fabricante neerlandés de equipo de litografía, enfrenta restricciones similares (EUV prohibido a China desde 2019; DUV avanzado restringido en 2023-2024). Sirve para contrastar: en su caso el peso de China *subió* (de 13.8% en 2022 a 36.1% en 2024) por compras anticipadas antes de las restricciones, y bajó a 29.1% en 2025 (ASML, 2023-2026).


## 1.7 Unidad de análisis

- **Unidad principal:** la exposición de Nvidia al mercado chino, medida con sus ingresos por región y por mercado (años fiscales 2020 a 2027-T2) y con el precio diario de su acción (enero 2019 a noviembre 2026).
- **Unidades secundarias:** tres rivales chinos que cotizan en bolsa (Cambricon, Hygon y SMIC) y ASML como caso de comparación.
- **Fronteras del caso:** no se analizan la tecnología de los chips ni la política exterior en sí; sólo su efecto observable en ingresos, en la acción y en los rivales.

## 1.8 Métodos de recolección y análisis (resumen)

El diseño del caso sigue las pautas del Banco Interamericano de Desarrollo (2011): antecedentes, propósito, pregunta de reflexión, unidad de análisis y métodos.

- **Recolección:** análisis de documentos oficiales (reportes 10-K, 10-Q y 20-F ante la SEC), bases de datos de precios (Yahoo Finance) y de la industria (SIA), y notas de prensa para fechar los eventos. Usar varias fuentes permite contrastar los hallazgos. El detalle está en Prepare y en los anexos.
- **Análisis:** (1) codificación de los 12 eventos regulatorios por origen (EE.UU. o China) y tipo (restricción o apertura), al estilo del análisis de contenido; (2) comparación de promedios por régimen regulatorio; (3) estudio de eventos sobre la acción; (4) descomposición del crecimiento por región; (5) índices de crecimiento de rivales. Cada hallazgo se contrasta con explicaciones alternativas (por ejemplo, movimientos del mercado en general).

## 1.9 Precisión sobre una cifra muy citada

Jensen Huang, director general de Nvidia, ha dicho que la participación de Nvidia en el mercado chino de chips de IA pasó de "95% a 0". Esa cifra se refiere a **participación de mercado** dentro de China, no al **peso de China en los ingresos** de Nvidia. Son métricas distintas y no se deben mezclar en el reporte. *(Pendiente: citar la fuente exacta de la declaración.)*