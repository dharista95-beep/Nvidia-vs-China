"""Fase 4b · Modelo para decidir.

Un modelo sencillo (y honesto) entrenado con las ventas trimestrales de Nvidia:
1. Se entrenan varios modelos y se elige el que mejor pronosticó trimestres pasados que no había visto.
2. El elegido proyecta las ventas del próximo año.
3. Esa proyección se combina con escenarios para China (que elige el usuario).
4. Una regla de decisión, con los KPIs de la fase Actuar, sugiere qué hacer al inversionista.

Con 28 trimestres no tiene sentido un modelo complejo: se sobreajustaría. Por eso se usan modelos de
tendencia simples y se mide su error con datos que no usaron para entrenar.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import analisis as A
import estilos as E

N_VAL, N_PRUEBA, H = 8, 4, 4
NOMBRE_CORTO = {"ingenuo": "Ingenuo", "crecimiento": "Crecimiento promedio", "tendencia": "Tendencia"}
EXPLICA_MODELO = {
    "ingenuo": "supone que el próximo trimestre se vende lo mismo que el último",
    "crecimiento": "toma cuánto crecieron en promedio las ventas en los últimos trimestres y supone que seguirán creciendo a ese ritmo",
    "tendencia": "traza la línea recta que mejor se ajusta a las ventas recientes (en escala de %) y la prolonga",
}


def render(D):
    q, px, ev = D["q"], D["px"], D["ev"]
    t = A.serie_total(q)
    y = t.total.values

    E.titulo("Fase 4b · Modelo para decidir",
             "Entrenamos un modelo con las ventas de Nvidia, lo ponemos a prueba y lo combinamos con escenarios de China "
             "para sugerir una decisión al inversionista.")
    st.markdown('<div class="nv-pregunta"><div class="nv-pq">¿Qué hace este modelo, en 4 pasos?</div>'
                '1) <b>Aprende</b> del pasado cuánto suelen crecer las ventas de Nvidia. '
                '2) Lo <b>ponemos a prueba</b> con trimestres que no vio, para saber cuánto se equivoca. '
                '3) <b>Proyecta</b> las ventas del próximo año. '
                '4) Junto con <b>escenarios para China</b> que tú eliges, aplica una <b>regla de decisión</b> clara.</div>',
                unsafe_allow_html=True)
    st.warning("Es una **proyección, no una predicción segura**: supone que el futuro se parece al pasado reciente. "
               "No explica causas (no dice *por qué* crecen las ventas) y no es asesoría de inversión.")

    # ------------------------------------------------------------------ Paso 1
    E.seccion("Paso 1 · Entrenar y elegir el modelo",
              f"Probamos 3 tipos de modelo, cada uno aprendiendo de los últimos 4, 8 o 12 trimestres. Para elegir, cada modelo "
              f"pronostica uno por uno {N_VAL} trimestres pasados usando sólo lo que se sabía antes (<b>validación</b>). "
              f"Los últimos {N_PRUEBA} trimestres se guardan aparte y sólo se usan al final para medir el error del elegido (<b>prueba</b>).")
    res = A.elegir_modelo(y, N_VAL, N_PRUEBA)
    mejor = res.iloc[0]
    n = len(y)
    v0, p0 = n - N_PRUEBA - N_VAL, n - N_PRUEBA
    E.tarjetas([
        ("Modelo elegido", f"{NOMBRE_CORTO[mejor.modelo]} ({int(mejor.ventana)} trim.)" if mejor.modelo != "ingenuo" else "Ingenuo",
         f"Aprende con los últimos {int(mejor.ventana)} trimestres", "azul", "🏆"),
        ("Error en validación (MAPE)", f"{mejor.error_validacion_pct:.1f}%",
         f"MAE {mejor.mae_validacion:,.0f} · RMSE {mejor.rmse_validacion:,.0f} MUSD. {t.periodo[v0]} a {t.periodo[p0-1]} (con esto se eligió)", "gris", "🧪"),
        ("Error en prueba (MAPE)", f"{mejor.error_prueba_pct:.1f}%",
         f"MAE {mejor.mae_prueba:,.0f} · RMSE {mejor.rmse_prueba:,.0f} MUSD. {t.periodo[p0]} a {t.periodo[n-1]} (datos que no vio)", "verde", "✅"),
        ("Datos de entrenamiento", f"{n} trimestres", f"{t.periodo[0]} a {t.periodo[n-1]}", "blanco", "📚"),
    ])
    tabla = res.copy()
    tabla["Modelo"] = [f"{NOMBRE_CORTO[m]}" for m in tabla.modelo]
    tabla["Aprende con"] = ["último trim." if m == "ingenuo" else f"últimos {w} trim." for m, w in zip(tabla.modelo, tabla.ventana)]
    cols_err = []
    for nombre, et in [("validacion", "valid."), ("prueba", "prueba")]:
        tabla[f"MAPE {et}"] = tabla[f"error_{nombre}_pct"].map("{:.1f}%".format)
        tabla[f"MAE {et}"] = tabla[f"mae_{nombre}"].map("{:,.0f}".format)
        tabla[f"RMSE {et}"] = tabla[f"rmse_{nombre}"].map("{:,.0f}".format)
        cols_err += [f"MAPE {et}", f"MAE {et}", f"RMSE {et}"]
    tabla["Lugar"] = [E.badge("Elegido", "verde") if i == 0 else str(i + 1) for i in range(len(tabla))]
    E.tabla(tabla[["Lugar", "Modelo", "Aprende con"] + cols_err], html_cols=("Lugar",), derecha=tuple(cols_err))
    st.caption("MAE y RMSE en millones de dólares. 'valid.' = validación.")
    st.markdown('''<div class="nv-explica"><b>Las tres formas de medir el error</b> (todas: mientras más chico, mejor)<br>
<b>MAPE</b> (error porcentual promedio): en promedio, ¿por qué porcentaje de las ventas reales se equivocó? 5% = se equivocó por 5%.
Es el que usamos para <b>elegir</b> el modelo, porque las ventas pasaron de ~3 mil a ~96 mil millones por trimestre y un error en dinero
pesaría mucho más en los trimestres recientes; el porcentaje los trata parejo.<br>
<b>MAE</b> (error absoluto promedio): lo mismo, pero en <b>millones de dólares</b>. Es el más fácil de imaginar: "en promedio, se equivocó por tantos millones".<br>
<b>RMSE</b> (raíz del error cuadrático medio): también en millones, pero <b>castiga más los errores grandes</b>. Si el RMSE es mucho mayor
que el MAE, quiere decir que el modelo tuvo algún error grande aislado (por ejemplo, el trimestre de la restricción del H20).
<span class="nv-clave"><b>¿Y la matriz de confusión?</b> No aplica aquí. La matriz de confusión sirve para modelos de <b>clasificación</b>,
que eligen entre categorías (por ejemplo "sube" o "baja") y se cuenta cuántas veces acertaron cada una. Nuestro modelo es de
<b>regresión</b>: pronostica un número (las ventas), así que se evalúa con qué tan lejos quedó ese número del real, que es justo lo que miden MAPE, MAE y RMSE.</span></div>''', unsafe_allow_html=True)
    mismo = all(res[c].idxmin() == 0 for c in ["error_validacion_pct", "mae_validacion", "rmse_validacion"])
    coincide = ("Además es el mejor en validación con las tres medidas, así que la elección no depende de cuál usemos." if mismo
                else "Con MAE o RMSE el orden cambia un poco; nos quedamos con el MAPE por la razón explicada arriba.")
    E.explicacion("La tabla está ordenada por el MAPE de validación, que es con lo que elegimos; las columnas de prueba son el 'examen final' "
                  "con trimestres que ningún modelo usó para entrenar ni para ser elegido.",
                  f"Ganó el modelo de <b>{NOMBRE_CORTO[mejor.modelo].lower()}</b>, que {EXPLICA_MODELO[mejor.modelo]}. "
                  f"En validación se equivocó {mejor.error_validacion_pct:.1f}% en promedio (unos {mejor.mae_validacion:,.0f} millones por trimestre) "
                  f"y en prueba {mejor.error_prueba_pct:.1f}% (unos {mejor.mae_prueba:,.0f} millones). {coincide} Ojo: la prueba son sólo {N_PRUEBA} trimestres, así que ese número puede ser suerte; "
                  "el de validación es más realista. El modelo 'ingenuo' sirve de referencia: cualquier modelo que no le gane no vale la pena.")

    ver = st.selectbox("Ver cómo le fue a un modelo", range(len(res)), format_func=lambda i: f"{tabla.Modelo[i]} · {tabla['Aprende con'][i]}")
    m_sel, w_sel = res.modelo[ver], int(res.ventana[ver])
    hist = A.prueba_historica(y, m_sel, w_sel, v0, n)
    hist["periodo"] = t.periodo[hist.i].values
    f = go.Figure()
    f.add_trace(go.Scatter(x=t.periodo, y=y / 1000, name="Ventas reales", mode="lines+markers", line=dict(color=E.GRIS, width=2), marker=dict(size=7)))
    f.add_trace(go.Scatter(x=hist.periodo, y=hist.pronostico / 1000, name="Pronóstico del modelo (sólo con datos anteriores)",
                           mode="markers", marker=dict(color=E.NARANJA, size=11, symbol="diamond")))
    f.add_vrect(x0=t.periodo[v0], x1=t.periodo[p0 - 1], fillcolor="#EEF4FB", opacity=0.6, line_width=0, layer="below",
                annotation_text="validación", annotation_position="top left")
    f.add_vrect(x0=t.periodo[p0], x1=t.periodo[n - 1], fillcolor="#EEF8F3", opacity=0.8, line_width=0, layer="below",
                annotation_text="prueba", annotation_position="top left")
    f.update_yaxes(title="Ventas del trimestre (miles de millones de USD)")
    E.mostrar(E.fig(f, "Lo que pronosticó el modelo vs. lo que realmente pasó", 420, leyenda=""))
    E.explicacion("La línea gris son las ventas reales. Los rombos naranjas son lo que el modelo pronosticó para cada trimestre "
                  "usando sólo información de antes. La zona azul es la validación y la verde la prueba.",
                  "Mientras más cerca estén los rombos de la línea gris, mejor. Cuando hay un salto inesperado (por ejemplo, la "
                  "restricción del H20 en 2025), todos los modelos fallan: un modelo de tendencia no puede anticipar una regla nueva.")

    # ------------------------------------------------------------------ Paso 2
    E.seccion("Paso 2 · Proyectar las ventas del próximo año",
              "El modelo elegido se entrena con todos los trimestres y proyecta los próximos 4. Puedes cambiar el crecimiento si "
              "quieres un escenario más conservador.")
    p2 = A.pronostico(y, mejor.modelo, int(mejor.ventana), 2)
    g_modelo = float(100 * (p2[1] / p2[0] - 1))       # crecimiento por trimestre que implica el modelo
    g = st.slider("Crecimiento por trimestre que se supone (%)", -10.0, 30.0, round(g_modelo, 1), 0.5,
                  help=f"El modelo estima {g_modelo:.1f}% por trimestre. Muévelo para ver un futuro más lento o más rápido.")
    proy = y[-1] * (1 + g / 100) ** np.arange(1, H + 1)
    val = A.prueba_historica(y, mejor.modelo, int(mejor.ventana), v0, p0)
    s = float(np.sqrt(np.mean(np.log(val.pronostico / val.real) ** 2)))   # tamaño típico del error (en escala log)
    banda = 1.96 * s * np.sqrt(np.arange(1, H + 1))
    etiquetas = []
    fy, tri = int(t.periodo.iloc[-1][2:6]), int(t.periodo.iloc[-1][-1])
    for _ in range(H):
        tri += 1
        if tri == 5:
            fy, tri = fy + 1, 1
        etiquetas.append(f"FY{fy}-Q{tri}")
    f = go.Figure()
    reciente = t.iloc[-12:]   # sólo los últimos 3 años, para que se lea bien
    f.add_trace(go.Scatter(x=reciente.periodo, y=reciente.total / 1000, name="Ventas reales", mode="lines+markers", line=dict(color=E.AZUL, width=2)))
    xs = [t.periodo.iloc[-1]] + etiquetas
    f.add_trace(go.Scatter(x=xs + xs[::-1], y=list(np.r_[y[-1], proy * np.exp(banda)] / 1000) + list((np.r_[y[-1], proy * np.exp(-banda)] / 1000)[::-1]),
                           fill="toself", fillcolor="rgba(235,104,52,0.15)", line=dict(width=0), mode="lines", name="Rango probable", hoverinfo="skip"))
    f.add_trace(go.Scatter(x=xs, y=np.r_[y[-1], proy] / 1000, name="Proyección", mode="lines+markers",
                           line=dict(color=E.NARANJA, dash="dash", width=2), marker=dict(size=8)))
    f.update_yaxes(title="Ventas del trimestre (miles de millones de USD)")
    E.mostrar(E.fig(f, f"Si el crecimiento sigue en {g:.1f}% por trimestre, el próximo año Nvidia vendería {proy.sum()/1000:,.0f} mil millones", 420, leyenda=""))
    E.explicacion("Azul: lo que ya pasó (últimos 3 años). Naranja punteado: la proyección. La sombra naranja es el rango donde probablemente caería "
                  "el dato real, según qué tanto se equivocó el modelo en la validación; se abre más mientras más lejos miramos.",
                  f"Comparado con los últimos 4 trimestres ({y[-H:].sum()/1000:,.0f} mil millones), la proyección implica un cambio de "
                  f"{100*(proy.sum()/y[-H:].sum()-1):+.0f}%. Es sólo una extrapolación del ritmo reciente: si la demanda de IA se frena, "
                  "o hay una regla nueva, el número real puede quedar muy por debajo.")

    # ------------------------------------------------------------------ Paso 3
    E.seccion("Paso 3 · Escenarios para China",
              "Tú eliges qué tanto pesaría China en cada escenario y qué tan probable crees que es cada uno. "
              "Los valores iniciales salen de los datos: 1.5% (cierre), 8.2% (el último trimestre) y 15% (como en 2024).")
    defaults = [("A. Se cierra todo", 1.5, 30), ("B. Apertura limitada (hoy)", 8.2, 60), ("C. Apertura amplia", 15.0, 10)]
    cols = st.columns(3)
    esc = []
    for c, (nom, pct0, p0_) in zip(cols, defaults):
        with c.container(border=True):
            st.markdown(f"**{nom}**")
            pct = st.slider("China, % de las ventas", 0.0, 30.0, pct0, 0.5, key=f"pct{nom}")
            prob = st.slider("Probabilidad que le doy (%)", 0, 100, p0_, 5, key=f"prob{nom}")
            esc.append((nom, pct, prob))
    probs = np.array([e[2] for e in esc], dtype=float)
    if probs.sum() == 0:
        st.error("Al menos un escenario debe tener probabilidad mayor que cero.")
        return
    probs = probs / probs.sum()
    tot = proy.sum()
    dfe = pd.DataFrame({"Escenario": [e[0] for e in esc], "pct": [e[1] for e in esc], "prob": probs})
    dfe["china_musd"] = tot * dfe.pct / 100
    pct_esperado = float((dfe.pct * dfe.prob).sum())
    china_esperada = tot * pct_esperado / 100
    if abs(sum(e[2] for e in esc) - 100) > 0.5:
        st.caption(f"Las probabilidades suman {sum(e[2] for e in esc)}%; las reescalamos para que sumen 100%.")
    E.tarjetas([("Peso esperado de China", f"{pct_esperado:.1f}%", "promedio de los escenarios, pesado por su probabilidad", "rosa", "🇨🇳"),
                ("Ventas esperadas en China (próximo año)", f"{china_esperada/1000:,.1f} mil MUSD", f"de {tot/1000:,.0f} mil millones proyectados", "azul", "💵"),
                ("Lo que se juega entre A y C", f"{(dfe.china_musd.max()-dfe.china_musd.min())/1000:,.1f} mil MUSD", "diferencia entre el mejor y el peor escenario", "gris", "⚖️")])
    f = go.Figure(go.Bar(x=dfe.Escenario, y=dfe.china_musd / 1000, marker_color=[E.NARANJA, E.GRIS, E.AZUL],
                         text=[f"{v/1000:,.1f} mil M · prob. {p:.0%}" for v, p in zip(dfe.china_musd, dfe.prob)], textposition="outside"))
    f.update_yaxes(title="Ventas en China el próximo año (miles de millones de USD)")
    E.mostrar(E.fig(f, "Cuánto le vendería Nvidia a China el próximo año en cada escenario", 360, unificado=False))
    E.explicacion("Cada barra multiplica las ventas proyectadas del paso 2 por el peso de China que elegiste para ese escenario. "
                  "Arriba de cada barra está la probabilidad que le diste.",
                  f"En el promedio pesado, China aportaría {pct_esperado:.1f}% de las ventas. Así se ve cuánto dinero está realmente "
                  "en juego con China, comparado con el tamaño total de la empresa.")

    # ------------------------------------------------------------------ Paso 4
    E.seccion("Paso 4 · Regla de decisión para el inversionista",
              "Cada regla usa un resultado del modelo o un indicador de la fase Actuar. La recomendación final sale de combinarlas.")
    ult = q[q.base == "sede_cliente"].iloc[-1]
    car_r = A.estudio_eventos(px, ev, "SP500", (-1, 1)).query("tipo == 'Restricción'").CAR_pct.mean()
    camb = D["riv"].set_index(["empresa", "anio"]).crec_anual_pct[("Cambricon", 2025)]
    crece = proy.sum() > y[-H:].sum()
    p_cierre = dfe.prob.iloc[0] * 100
    reglas = [
        ("¿Las ventas seguirán creciendo?", f"Proyección {100*(proy.sum()/y[-H:].sum()-1):+.0f}% vs. últimos 4 trimestres", crece,
         "Sí: el negocio sigue creciendo sin depender de China." if crece else "No: el negocio se frena; hay que revisar la posición."),
        ("¿China pesa menos de 10%?", f"Peso esperado {pct_esperado:.1f}%", pct_esperado < 10,
         "Sí: China no cambia el valor de la empresa. No pagar de más por noticias de apertura." if pct_esperado < 10
         else "No: China sí importa; seguir de cerca cada permiso."),
        ("¿La probabilidad de cierre es de 30% o más?", f"Cierre {p_cierre:.0f}%", p_cierre >= 30,
         f"Sí: conviene protegerse en fechas de anuncio; una mala noticia ha costado en promedio {car_r:.1f}% en 3 días." if p_cierre >= 30
         else "No: el riesgo de cierre es bajo; no hace falta protección especial."),
        ("¿EE.UU. pesa más de 60%?", f"EE.UU. {ult.pct_eeuu:.1f}% ({ult.periodo})", ult.pct_eeuu > 60,
         "Sí: el riesgo ahora es la concentración en EE.UU. y pocos clientes; vigilarlo cada trimestre." if ult.pct_eeuu > 60
         else "No: la concentración en EE.UU. está en un nivel razonable."),
        ("¿Los competidores chinos crecen más de 50%?", f"Cambricon {camb:+.0f}% (2025)", camb > 50,
         "Sí: tratar la pérdida de China como permanente." if camb > 50 else "No: todavía hay espacio para que Nvidia regrese."),
    ]
    tr = pd.DataFrame(reglas, columns=["Regla", "Dato", "ok", "Qué implica"])
    tr["¿Se cumple?"] = [E.badge("Sí", "azul") if o else E.badge("No", "gris") for o in tr.ok]
    E.tabla(tr[["Regla", "Dato", "¿Se cumple?", "Qué implica"]], html_cols=("¿Se cumple?",))

    if not crece:
        veredicto, color, detalle = "Reducir o revisar la posición", "rosa", "La proyección no muestra crecimiento; el motivo para mantener se debilita."
    elif p_cierre >= 30:
        veredicto, color, detalle = "Mantener, con protección en fechas de riesgo", "azul", \
            "El negocio crece sin China, pero una mala noticia puede costar varios puntos en pocos días."
    else:
        veredicto, color, detalle = "Mantener", "verde", "El negocio crece y el riesgo de China es bajo con los supuestos elegidos."
    st.markdown(E.tarjeta("Recomendación con los supuestos elegidos", veredicto, detalle, color, "🧭"), unsafe_allow_html=True)
    st.markdown(f'<div class="nv-explica"><b>Y para Nvidia:</b> presupuestar el próximo año con China en cero para centros de datos y '
                f'tratar los ~{china_esperada/1000:,.1f} mil millones esperados como un extra. Fabricar para China sólo contra pedidos '
                f'con permiso de los dos gobiernos.</div>', unsafe_allow_html=True)
    E.explicacion("Mueve los supuestos de los pasos 2 y 3 (crecimiento, peso de China y probabilidades) y mira cómo cambian las reglas "
                  "y la recomendación. Así se ve qué supuestos son los que realmente mueven la decisión.",
                  "Con los datos actuales, la conclusión casi no depende de China: lo que la cambiaría es que el crecimiento total se "
                  "frenara. Eso coincide con el análisis: China ya es un riesgo de volatilidad, no del tamaño del negocio.")
    with st.expander("Limitaciones del modelo"):
        st.markdown(f"""
- **Pocos datos:** {n} trimestres. Por eso usamos modelos sencillos; uno complejo 'memorizaría' el pasado y fallaría en el futuro.
- **Extrapola el pasado:** supone que el ritmo reciente sigue. No puede anticipar una regla nueva, un freno de la demanda de IA ni la pérdida de un cliente grande.
- **No explica causas:** dice cuánto podrían ser las ventas, no por qué.
- **La prueba tiene sólo {N_PRUEBA} trimestres**, así que su error es poco estable; el de validación ({N_VAL} trimestres) es más confiable.
- **Los escenarios de China y sus probabilidades son supuestos** de quien usa la app, no salen del modelo.
- **Las reglas de decisión y sus umbrales (10%, 30%, 60%, 50%) son propuestas del equipo**, no estándares del mercado.
- Ejercicio académico; **no es asesoría de inversión**.
""")
