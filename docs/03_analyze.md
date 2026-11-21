# FASE 4. ANALYZE (Analizar)

> Sección autocontenida. Cálculos en `notebooks/02_analyze_share.ipynb`; resultados en `data/resultados/`. Todas las cifras en millones de dólares (MUSD) salvo que se indique otra cosa. **Ningún resultado de esta sección prueba causalidad**: se describen asociaciones en el tiempo.

## 4.1 Enfoque

Fuentes: NVIDIA (2020-2026), ASML (2020-2026), Yahoo Finance (2026) y Semiconductor Industry Association (2021-2026); ver referencias.

| Pregunta | Técnica | Datos |
|---|---|---|
| P1. ¿Cuánto cambió el peso de China tras cada ronda de controles? | Comparación de promedios por "régimen" regulatorio y variación interanual | Ingresos trimestrales por región (SEC) |
| P2. ¿Cómo reaccionó la acción en los días de anuncio? | Estudio de eventos con modelo de mercado | Precios diarios NVDA, S&P 500 y SOX; 12 eventos |
| P3. ¿Otras regiones y Data Center compensaron la pérdida? | Descomposición del cambio anual de ingresos por región | Ingresos anuales por región; ventas globales SIA |
| P4. ¿Crecieron los rivales chinos en los mismos periodos? | Índices de crecimiento (2022 = 100) y rendimiento bursátil | Ingresos y precios de Cambricon, Hygon y SMIC |

Para P1 se definieron cuatro regímenes según el trimestre fiscal en que entró en vigor cada regla (decisión A-01):

| Régimen | Trimestres fiscales | Qué podía vender Nvidia en China |
|---|---|---|
| R0 Sin controles | FY2020-T3 a FY2023-T2 | Todo su catálogo (A100, H100) |
| R1 Controles 2022 | FY2023-T3 a FY2024-T3 | Versiones recortadas A800 y H800 |
| R2 Controles oct-2023 | FY2024-T4 a FY2026-T1 | H20 |
| R3 Licencia H20 / H200 | FY2026-T2 a FY2027-T2 | Prácticamente nada de Data Center; H200 sólo con licencia y freno de China |

## 4.2 P1. El peso de China cayó en cada régimen, pero hasta 2025 fue por dilución, no por pérdida

| Base | Régimen | Trimestres | China promedio (MUSD) | Total promedio (MUSD) | % China promedio | Rango % |
|---|---|---|---|---|---|---|
| Facturación | R0 Sin controles | 12 | 1,356 | 5,392 | **25.0%** | 22.1 a 28.4 |
| Facturación | R1 Controles 2022 | 5 | 2,092 | 10,160 | **20.0%** | 15.8 a 22.2 |
| Facturación | R2 Controles oct-2023 | 6 | 4,096 | 32,777 | **12.1%** | 8.8 a 15.4 |
| Facturación | R3 Licencia H20 | 1 | 2,769 | 46,743 | **5.9%** | 5.9 |
| Sede del cliente | R2 Controles oct-2023 | 3 | 8,540 | 39,492 | **21.7%** | 19.9 a 23.2 |
| Sede del cliente | R3 Licencia H20 / H200 | 5 | 4,490 | 69,942 | **6.4%** | 4.5 a 8.5 |

**Hallazgos:**
1. **El peso de China bajó en cada régimen**: de 25.0% sin controles a 20.0%, 12.1% y 5.9% (base facturación).
2. **Hasta 2025 los ingresos de China *crecieron* en dólares** (de 1,356 a 4,096 MUSD promedio por trimestre). El peso cayó porque el total creció mucho más rápido (de 5,392 a 32,777 MUSD), impulsado por la demanda de IA en EE.UU. Es decir, en R1 y R2 la caída fue principalmente **dilución**.
3. **En R3 (desde abril de 2025) sí hubo pérdida absoluta**: con la base sede del cliente, China pasó de 8,540 a 4,490 MUSD promedio por trimestre (−47%). Los ingresos de China cayeron 63.5%, 60.9% y 52.9% interanual en los tres trimestres siguientes, mientras el total crecía entre 62% y 85%.
4. El trimestre posterior a cada regla muestra el golpe más claro: en FY2024-T4 (justo después de oct-2023) China bajó de 22.2% a 8.8%, y en FY2026-T2 (después de abril de 2025) de 21.9% a 8.5%.
5. **Señal a vigilar:** en FY2027-T2 China subió a 7,880 MUSD (8.2%). Nvidia reporta que el H200 vendido a China fue menos del 1% de Data Center, así que ese repunte probablemente viene de clientes con sede en China que compran para otros países o de otros productos. Con los datos públicos no se puede saber.

## 4.3 P2. Las malas noticias regulatorias pesan más que las buenas, y cada vez menos

Estudio de eventos (A-02): modelo de mercado estimado con 240 días hábiles previos; rendimiento anormal acumulado (CAR) en la ventana de −1 a +1 días.

| ID | Fecha de reacción | Evento | Tipo | Día 0 NVDA | CAR vs S&P 500 | t | CAR vs SOX | t |
|---|---|---|---|---|---|---|---|---|
| E1 | 01-sep-2022 | 8-K: A100/H100 requieren licencia | Restricción | −7.7% | **−8.4%** | **−2.26** | **−6.5%** | **−2.52** |
| E2 | 07-oct-2022 | Reglas BIS del 7 de octubre | Restricción | −8.0% | −1.5% | −0.37 | +2.5% | 0.91 |
| E3 | 17-oct-2023 | Actualización BIS (A800/H800) | Restricción | −4.7% | −7.7% | −1.85 | **−6.6%** | **−2.11** |
| E4 | 09-dic-2024 | China investiga a Nvidia (antimonopolio) | Restricción | −2.6% | −5.7% | −1.36 | −4.9% | −1.45 |
| E5 | 13-ene-2025 | Regla "AI Diffusion" | Restricción | −2.0% | −3.1% | −0.71 | −4.3% | −1.21 |
| E6 | 16-abr-2025 | H20 requiere licencia | Restricción | −6.9% | −2.3% | −0.49 | −3.7% | −1.02 |
| E7 | 15-jul-2025 | Nvidia retomará ventas de H20 | Apertura | +4.0% | +3.8% | 0.86 | +3.6% | 1.04 |
| E8 | 11-ago-2025 | Acuerdo del 15% para EE.UU. | Apertura | −0.4% | −2.2% | −0.55 | −2.9% | −0.90 |
| E9 | 17-sep-2025 | China pide no comprar Nvidia | Restricción | −2.6% | −1.5% | −0.39 | −4.7% | −1.53 |
| E10 | 08-dic-2025 | EE.UU. autoriza H200 (25%) | Apertura | +1.7% | +1.2% | 0.33 | −1.3% | −0.41 |
| E11 | 14-ene-2026 | Aduanas chinas frenan el H200 | Restricción | −1.4% | +2.0% | 0.54 | −1.0% | −0.31 |
| E12 | 19-ago-2026 | China permite H200 limitado | Apertura | −1.0% | −0.9% | −0.31 | 0.0% | 0.01 |

**Promedios:** anuncios de restricción (8): CAR −3.5% contra S&P 500 y −3.7% contra SOX. Anuncios de apertura (4): +0.5% y −0.1%.

**Hallazgos:**
1. **Asimetría:** en promedio una restricción restó cerca de 3.5% de valor anormal en tres días; una apertura casi no sumó. El mercado parece tratar las aperturas como poco creíbles o poco duraderas *(interpretación, no comprobada)*.
2. **La reacción se fue haciendo más pequeña:** los eventos de 2022-2023 tuvieron CAR de −7.7% a −8.4%; los de 2025-2026 se quedaron entre −3% y +4%. Esto coincide con que China pesa cada vez menos en los ingresos.
3. **Sólo E1 es estadísticamente significativo contra el S&P 500** (y E1 y E3 contra SOX). Con 12 eventos, la evidencia es indicativa.
4. **La referencia importa:** el 7-oct-2022 NVDA cayó 8.0%, pero todo el mercado cayó ese día (dato de empleo de EE.UU.), así que el efecto anormal fue sólo −1.5%. En abril de 2025 la guerra arancelaria movía todo el mercado. Usar sólo el rendimiento bruto exageraría el efecto.

## 4.4 P3. EE.UU. compensó con creces a China, pero creó otra concentración

| Periodo (base) | Cambio total | EE.UU. | Taiwán | China | Otros |
|---|---|---|---|---|---|
| FY2022→FY2025 (facturación) | +103,583 | +56,908 (55%) | +12,029 (12%) | **+9,997 (10%)** | +24,649 (24%) |
| FY2025→FY2026 (sede del cliente) | +85,441 | +72,135 (84%) | +18,745 (22%) | **−5,371 (−6%)** | −68 (0%) |

**Hallazgos:**
1. La pérdida de China en FY2026 (−5,371 MUSD) equivale a apenas 6% del crecimiento de ese año; el aumento de EE.UU. por sí solo fue 13 veces mayor que lo perdido en China.
2. **La dependencia se movió de mercado:** EE.UU. pasó de 51.8% (FY2024) a 69.3% (FY2026) de los ingresos (base sede del cliente), y en el 3T FY2026 cuatro clientes directos concentraron 22%, 15%, 13% y 11% de los ingresos (Nvidia, 2025).
3. **Data Center es casi todo el negocio:** pasó de 39.4% de los ingresos en FY2022 a 89.7% en FY2026. Los controles atacan justamente ese segmento.
4. Contexto de industria: los ingresos de Nvidia equivalen a cerca de 27% de las ventas mundiales de semiconductores de 2025 (791,700 MUSD según la SIA), frente a 4.7% en 2022. *(Comparación aproximada: el año fiscal de Nvidia termina en enero.)*

## 4.5 P4. Los rivales chinos crecieron más rápido justo cuando Nvidia perdió acceso (asociación)

Ingresos, índice 2022 = 100 (moneda local):

| Año | Cambricon | Hygon | SMIC |
|---|---|---|---|
| 2022 | 100 | 100 | 100 |
| 2023 | 97 | 117 | 87 |
| 2024 | 161 | 179 | 110 |
| 2025 | **891** | **281** | 128 |

Rendimiento bursátil del 31-ago-2022 (primer control) al 19-nov-2026: Cambricon +2,258%, NVDA +871%, Hygon +260%, SOX +252%, SMIC (Shanghái) +204%, S&P 500 +81%.

**Hallazgos:**
1. El salto más grande de Cambricon (+453% en 2025) coincide con el año en que el H20 requirió licencia y China pidió a sus empresas no comprar Nvidia.
2. **Esto no prueba que los controles causaran el crecimiento.** En el mismo periodo hubo subsidios estatales, la ola de demanda de IA en China y otras políticas. Con 4 años de datos no se puede separar el efecto.
3. SMIC, la fábrica que produce para varios de estos diseñadores, creció mucho menos (+28%), lo que sugiere que la capacidad de fabricación avanzada en China sigue siendo un cuello de botella *(interpretación)*.

## 4.6 Recuadro comparativo: ASML

ASML, fabricante neerlandés de máquinas de litografía, enfrenta controles parecidos (EUV prohibido a China desde 2019; DUV avanzado restringido en 2023-2024). El peso de China en sus ventas pasó de 13.8% (2022) a 26.3% (2023) y 36.1% (2024), y bajó a 29.1% en 2025.

**Lección:** en ASML las restricciones anunciadas con anticipación provocaron **compras anticipadas** que inflaron temporalmente a China. En Nvidia, donde las reglas entraron en vigor casi de inmediato, el efecto fue el contrario. Para un inversionista, un aumento repentino del peso de China antes de una restricción es una **señal de riesgo**, no de fortaleza.

## 4.7 Limitaciones del análisis

- Dos bases geográficas no comparables (cambio de metodología de oct-2025); los regímenes se comparan dentro de cada base.
- La región es la del cliente directo, no la del uso final; reventa o contrabando no son visibles.
- El estudio de eventos tiene 12 eventos y varios coinciden con otras noticias.
- Rivales: 4 años de datos, fuente secundaria (Yahoo Finance), monedas distintas.
- Huawei, el rival más relevante, no publica datos de sus chips Ascend.
