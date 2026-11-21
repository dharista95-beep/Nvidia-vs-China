# FASE 5. SHARE (Compartir)

> Sección autocontenida. Las gráficas están en `figuras/` (PNG de alta resolución) y se generan con `notebooks/02_analyze_share.ipynb`.

## 5.1 Audiencia y mensaje

- **Audiencia:** dirección de estrategia de Nvidia e inversionistas (no especialistas en datos).
- **Mensaje central:** China dejó de ser un motor de crecimiento para Nvidia; su peso cayó de ~25% a menos de 10% de los ingresos. El golpe directo a los ingresos es pequeño frente al crecimiento total, pero cada anuncio de restricción sigue moviendo la acción y la dependencia se trasladó a EE.UU. y a unos pocos clientes.
- **Principios de diseño:** cada gráfica tiene un título que dice la conclusión, una sola escala, etiquetas directas, colores consistentes (azul = Nvidia/ventaja, naranja = China/restricción) y la fuente al pie.

## 5.2 Gráficas e interpretación

**Figura 1. Peso de China en los ingresos trimestrales** (`fig1_peso_china_trimestral.png`)
China pasó de ~25% de los ingresos antes de los controles a 4.5% en el punto más bajo (FY2026-T4) y 8.2% en el último dato. Cada línea vertical marca una regla; la caída más fuerte viene en el trimestre siguiente. Las dos líneas son dos formas distintas de contar (facturación y sede del cliente) y no se deben unir.

**Figura 2. De dónde vino el crecimiento en FY2026** (`fig2_descomposicion_regiones.png`)
En el año fiscal 2026 China restó 5,400 MUSD, pero EE.UU. sumó 72,100 y Taiwán 18,700. La pérdida de China quedó más que compensada; el riesgo nuevo es depender de EE.UU. (69% de los ingresos).

**Figura 3. Reacción de la acción a cada anuncio** (`fig3_estudio_eventos.png`)
Los anuncios de restricción (naranja) restaron en promedio 3.5% de valor anormal en tres días; las aperturas (azul) casi no sumaron. Las reacciones de 2022-2023 fueron las más grandes; las recientes son menores.

**Figura 4. Crecimiento de rivales chinos** (`fig4_rivales_chinos.png`)
Cambricon multiplicó por casi 9 sus ingresos entre 2022 y 2025; Hygon por casi 3. El salto coincide con la salida de Nvidia, pero es una asociación, no una prueba de causa.

**Figura 5. Recuadro ASML** (`fig5_asml_vs_nvidia.png`)
Con controles parecidos, el peso de China subió en ASML (compras anticipadas) y cayó en Nvidia. Un aumento súbito del peso de China puede anticipar una restricción.

## 5.3 Hallazgos clave para la presentación (una línea cada uno)

1. El peso de China cayó en cada ronda de controles: 25% → 20% → 12% → 6%.
2. Hasta 2025 fue dilución (China crecía, pero menos); desde abril de 2025 es pérdida real (−47% por trimestre).
3. La acción reacciona más a las malas noticias que a las buenas, y cada vez menos.
4. EE.UU. compensó la pérdida 13 veces, pero ahora concentra 69% de los ingresos.
5. Los rivales chinos crecieron más rápido justo cuando Nvidia perdió acceso (asociación).

---

# FASE 6. ACT (Actuar)

> Sección autocontenida. Las acciones se derivan de los hallazgos de Analyze. **El impacto descrito es esperado, no comprobado**: depende de decisiones regulatorias fuera del control de Nvidia y del inversionista.

## 6.1 Lecciones aprendidas

Las lecciones relacionan los resultados del caso con los factores que pudieron influir en ellos. Se presentan como relaciones observadas, no como causas comprobadas.

| # | Lección | Evidencia en el caso |
|---|---|---|
| L1 | **Adaptar un producto a una regla compra tiempo, no acceso permanente.** | A800/H800 y H20 fueron restringidos entre 12 y 15 meses después de su lanzamiento. |
| L2 | **Bajo controles cruzados, vender requiere dos llaves: la del país exportador y la del importador.** | Con licencias de EE.UU. para el H20, Nvidia sólo vendió ~60 MUSD porque China frenó las compras. |
| L3 | **Producir antes de tener certeza regulatoria convierte el riesgo político en pérdida contable.** | Cargos de 4,500 MUSD (H20) y 400 MUSD (H200). |
| L4 | **Un crecimiento fuerte en otros mercados puede ocultar la pérdida de uno.** | Hasta 2025, China crecía en dólares aunque su peso bajaba; la pérdida real apareció después. Hay que medir tanto el monto como el porcentaje. |
| L5 | **El mercado bursátil castiga las restricciones más de lo que premia las aperturas.** | CAR promedio −3.5% en restricciones y +0.5% en aperturas. |
| L6 | **Salir de un mercado deja espacio a competidores locales.** | Cambricon multiplicó por casi nueve sus ingresos entre 2022 y 2025 (asociación, no causa comprobada). |

**¿Qué podría hacerse diferente y mejor en una próxima ocasión?** Planear desde el inicio con el escenario más restrictivo, atar la producción a licencias aprobadas por ambos gobiernos, y medir la exposición en monto y en porcentaje cada trimestre. Las recomendaciones siguientes traducen estas lecciones en acciones.

## 6.2 Respuesta a la pregunta central

**¿Cómo debe Nvidia, o un inversionista, gestionar su exposición al mercado chino?**
Tratando a China como una **opción**, no como una base del negocio: planear con un escenario en el que China aporta cero a Data Center, invertir en China sólo contra licencias ya aprobadas por ambos gobiernos, y medir y cubrir la exposición de forma explícita. Al mismo tiempo, gestionar el riesgo nuevo que dejó la salida de China: la concentración en EE.UU. y en pocos clientes.

## 6.3 Recomendaciones para Nvidia

| # | Acción | Hallazgo que la respalda | Impacto esperado (no comprobado) |
|---|---|---|---|
| N1 | **Producir chips para China sólo con doble aprobación**: licencia de EE.UU. *y* señal clara de que China permitirá la importación. | Cargos por inventario de 4,500 MUSD (H20) y 400 MUSD (H200); China frenó el H200 aun con licencia de EE.UU. | Evitar nuevos cargos por inventario varado. |
| N2 | **Presupuestar con China = 0 en Data Center** y tratar cualquier venta como ingreso adicional. | China ya es 5-8% de los ingresos y la reacción del mercado a aperturas es casi nula. | Menos sorpresas negativas en la guía trimestral. |
| N3 | **Diversificar hacia "IA soberana"** (Europa, Medio Oriente, Japón, India) y nuevos clientes empresariales. | EE.UU. pasó de 52% a 69% de los ingresos; 4 clientes concentran ~60% en un trimestre. | Menor concentración por país y por cliente. |
| N4 | **Plan de escenarios regulatorios** con disparadores definidos (ver 6.5). | 12 eventos regulatorios en 4 años, de ambos gobiernos. | Respuesta más rápida y ordenada a cada nueva regla. |
| N5 | **Reportar la exposición a China de forma estable** (una sola base y, si es posible, ingresos por destino final). | El cambio de metodología de 2025 hace que China pese 19% o 13% en el mismo año según la base. | Menos incertidumbre para inversionistas. |

## 6.4 Recomendaciones para el inversionista

| # | Acción | Hallazgo que la respalda | Impacto esperado (no comprobado) |
|---|---|---|---|
| I1 | **Valuar a Nvidia sin China** y considerar cualquier apertura como potencial adicional. | Las aperturas casi no movieron la acción (+0.5% promedio) y varias se revirtieron. | Evitar pagar de más por noticias que no se materializan. |
| I2 | **Cubrir el riesgo de evento** en fechas regulatorias conocidas (actualizaciones de BIS, cumbres EE.UU.-China), por ejemplo con opciones o reduciendo temporalmente la posición. | Las restricciones restaron en promedio 3.5% en tres días (hasta 8.4%). | Menor caída de la cartera en días de anuncio. |
| I3 | **Vigilar la concentración**, no sólo a China: peso de EE.UU. y de los principales clientes en cada 10-Q. | 69% de los ingresos en EE.UU.; clientes de 11-22% cada uno. | Detectar a tiempo el riesgo que reemplazó al de China. |
| I4 | **Usar a los rivales chinos como termómetro**: si Cambricon y Hygon siguen creciendo >50% anual, tratar la pérdida de China como permanente. | Cambricon +453% y Hygon +57% en 2025. | Expectativas más realistas sobre un regreso a China. |
| I5 | **Desconfiar de aumentos súbitos del peso de China** en empresas de semiconductores. | Caso ASML: China subió a 36% por compras anticipadas antes de bajar. | Evitar comprar en el pico de un efecto temporal. |

*Nota: estas recomendaciones son parte de un ejercicio académico y no constituyen asesoría de inversión.*

## 6.5 Escenarios y disparadores

| Escenario | Qué tendría que pasar (disparador) | Peso de China esperado | Acción |
|---|---|---|---|
| A. Cierre total | Nueva regla de EE.UU. sobre H200, o China prohíbe formalmente importar Nvidia | ~0-3% | Mantener N2; liquidar inventario específico para China |
| B. Apertura limitada (base actual) | Licencias caso por caso y China aprueba compras puntuales | ~5-9% | Producir sólo contra pedidos aprobados (N1) |
| C. Apertura amplia | Acuerdo comercial EE.UU.-China que incluya chips de IA | >10% | Aumentar oferta de forma gradual, sin compromisos de inventario de largo plazo |

## 6.6 Plan de acción y KPIs

| Acción | Responsable | Plazo | KPI | Meta propuesta | Fuente del dato |
|---|---|---|---|---|---|
| N1 Doble aprobación | Operaciones y Legal | Inmediato | Cargos por inventario relacionados con China | 0 MUSD por trimestre | 10-Q / 10-K |
| N2 Presupuesto sin China | Finanzas | Próximo ciclo de guía | Diferencia entre guía e ingreso real atribuible a China | < 1% de los ingresos | Comunicado de resultados |
| N3 Diversificación | Ventas | 12 a 24 meses | % de ingresos fuera de EE.UU. y China; % del mayor cliente | > 30% fuera de EE.UU.; mayor cliente < 15% | 10-Q (región y clientes) |
| N4 Escenarios | Estrategia | 3 meses | Días entre una nueva regla y la guía actualizada | ≤ 5 días hábiles | Comunicados / 8-K |
| N5 Reporte estable | Relación con inversionistas | Próximo 10-K | Series regionales comparables publicadas | ≥ 8 trimestres re-expresados | 10-K |
| I2 Cobertura de eventos | Inversionista | Continuo | CAR de la cartera en días de anuncio | Menor que el CAR de NVDA sin cubrir | Precios diarios |
| I3/I4 Tablero de monitoreo | Inversionista | Trimestral | % China, % EE.UU., % mayor cliente, crecimiento de rivales | Revisión cada trimestre | `data/clean/` del proyecto |

*Las metas son propuestas del equipo para dar seguimiento; su cumplimiento y su efecto no están comprobados.*

## 6.7 Próximos pasos

1. Actualizar el tablero cada vez que Nvidia publique un 10-Q (el siguiente cubre ago-oct 2026).
2. Ampliar el estudio de eventos con más empresas (AMD, ASML) para separar el efecto sectorial del efecto Nvidia.
3. Buscar datos de destino final (por ejemplo, estadísticas de comercio de Taiwán y Singapur) para estimar ventas indirectas a China.
