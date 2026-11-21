"""Fase 4 · Analizar: una pestaña por pregunta, cada gráfica con su explicación."""
import pandas as pd
import plotly.express as px_
import plotly.graph_objects as go
import streamlit as st

import analisis as A
import estilos as E
import textos as T

MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
FUENTE_SEC = "Fuente: reportes de Nvidia a la SEC (10-K y 10-Q). China incluye Hong Kong."


def marcar_rondas(f, desde=None):
    """Líneas punteadas en cada ronda de restricciones."""
    for i, (fch, txt) in enumerate(A.RONDAS):
        if desde is not None and pd.Timestamp(fch) < pd.Timestamp(desde):
            continue
        f.add_shape(type="line", x0=fch, x1=fch, y0=0, y1=1, yref="paper", line=dict(color=E.GRIS, dash="dot", width=1))
        # Etiquetas a dos alturas para que no se encimen las que están cerca (2025)
        f.add_annotation(x=fch, y=1 if i % 2 == 0 else 0.93, yref="paper", text=txt, showarrow=False,
                         font=dict(size=11, color="#52514e"), yanchor="bottom", bgcolor="rgba(255,255,255,0.8)")
    return f


def lineas_por_base(q, col, bases):
    f = go.Figure()
    for b, color, dash in [("facturacion", E.AZUL, "solid"), ("sede_cliente", E.NARANJA, "dash")]:
        if b in bases:
            s = q[q.base == b]
            f.add_trace(go.Scatter(x=s.fin, y=s[col], name=A.NOMBRE_BASE[b], mode="lines+markers",
                                   line=dict(color=color, dash=dash, width=2), marker=dict(size=8),
                                   customdata=s.periodo, hovertemplate="%{customdata}: %{y:,.1f}<extra></extra>"))
    return f


def p1(D):
    q = D["q"]
    E.pregunta("P1", T.PREGUNTAS["P1"])
    c1, c2 = st.columns(2)
    medida = c1.radio("Ver en", ["% de las ventas", "Millones de dólares"], horizontal=True)
    bases = c2.multiselect("Forma de contar las ventas por país", list(A.NOMBRE_BASE), default=list(A.NOMBRE_BASE),
                           format_func=lambda b: A.NOMBRE_BASE[b])
    col = "pct_china" if medida.startswith("%") else "china"
    f = marcar_rondas(lineas_por_base(q, col, bases))
    f.update_yaxes(title="% de las ventas totales" if col == "pct_china" else "Ventas en China (millones de USD)", rangemode="tozero")
    tit = ("China pasó de ~25% a menos de 10% de las ventas de Nvidia" if col == "pct_china"
           else "En dólares, China siguió creciendo hasta 2025 y después se desplomó")
    E.mostrar(E.fig(f, tit, 460, leyenda="Forma de contar"))
    st.caption(FUENTE_SEC)
    if col == "pct_china":
        E.explicacion("Cada punto es un trimestre: qué parte de todo lo que vendió Nvidia fue a China. Las líneas grises "
                      "punteadas marcan cada ronda de restricciones. Hay dos líneas porque Nvidia cambió en 2025 la forma "
                      "de contar las ventas por país (ver Glosario); no se deben unir.",
                      "Después de cada restricción, el peso de China baja un escalón. El punto más bajo fue 4.5% a inicios "
                      "de 2026; con la apertura parcial del H200 subió un poco, a 8.2%.")
    else:
        E.explicacion("Cada punto es un trimestre: cuántos millones de dólares le vendió Nvidia a China.",
                      "Ojo con esta diferencia: hasta 2025 China seguía comprando <b>más</b> dólares cada año; su porcentaje "
                      "bajaba sólo porque el resto del mundo crecía muchísimo más rápido (a eso le llamamos dilución). "
                      "A partir de abril de 2025, con la restricción del H20, la caída ya es en dinero real.")

    # Promedio por régimen
    reg = A.tabla_regimenes(q)
    reg = reg[reg.base == "facturacion"]
    f = px_.bar(reg, x="regimen", y="pct_china_prom", text=reg.pct_china_prom.map("{:.0f}%".format),
                color_discrete_sequence=[E.AZUL],
                labels={"regimen": "", "pct_china_prom": "% promedio de las ventas que fueron a China"})
    E.mostrar(E.fig(f, "En promedio, cada ronda de reglas bajó a China un escalón: 25% → 20% → 12% → 6%", 360, unificado=False))
    E.explicacion("Agrupamos los trimestres según qué reglas estaban vigentes (un 'régimen') y sacamos el promedio de cada grupo. "
                  "Se usa sólo la forma de contar anterior, que es la que cubre todos los periodos.",
                  "La caída es constante en cada etapa. Esto muestra que pasó <b>después</b> de cada regla; por sí solo no "
                  "prueba que la regla sea la única causa.")


def p2(D):
    px, ev = D["px"], D["ev"]
    E.pregunta("P2", T.PREGUNTAS["P2"])
    c1, c2 = st.columns(2)
    mercado = c1.radio("Comparar contra", ["SP500", "SOX"], horizontal=True,
                       format_func=lambda m: {"SP500": "El mercado (S&P 500)", "SOX": "El sector de chips (SOX)"}[m])
    ventanas = {"3 días (un día antes, el día y uno después)": (-1, 1), "Sólo el día de la noticia": (0, 0),
                "7 días (tres antes y tres después)": (-3, 3)}
    vent = c2.radio("¿Cuántos días medir?", list(ventanas))
    res = A.estudio_eventos(px, ev, mercado, ventanas[vent])
    fch = pd.to_datetime(res.fecha)
    res["etiqueta"] = res.id + "  " + [f"{MES[m-1]}-{y}" for m, y in zip(fch.dt.month, fch.dt.year)]
    res["texto"] = res.CAR_pct.map("{:+.1f}%".format) + res.significativo_5pct.map({True: " *", False: ""})

    r_, a_ = res[res.tipo == "Restricción"], res[res.tipo == "Apertura"]
    E.tarjetas([("Malas noticias (restricciones)", f"{r_.CAR_pct.mean():+.1f}%", f"movimiento extra promedio, {len(r_)} noticias", "rosa", "🔻"),
                ("Buenas noticias (aperturas)", f"{a_.CAR_pct.mean():+.1f}%", f"movimiento extra promedio, {len(a_)} noticias", "azul", "🔺"),
                ("Movimientos claramente fuera de lo normal", f"{int(res.significativo_5pct.sum())} de {len(res)}", "marcados con * en la gráfica", "gris", "⭐")])

    f = px_.bar(res.iloc[::-1], x="CAR_pct", y="etiqueta", color="tipo", orientation="h", text="texto",
                color_discrete_map={"Restricción": E.NARANJA, "Apertura": E.AZUL},
                hover_data={"descripcion": True, "etiqueta": False, "texto": False, "tipo": False},
                labels={"CAR_pct": "Movimiento extra de la acción de Nvidia (%)", "etiqueta": "", "tipo": "Tipo de noticia",
                        "descripcion": "Qué pasó"})
    f.update_traces(textposition="outside")
    f.update_yaxes(categoryorder="array", categoryarray=list(res.etiqueta[::-1]))
    E.mostrar(E.fig(f, "Las malas noticias le quitan valor a la acción; las buenas casi no le suman", 540,
                    leyenda="Tipo de noticia", unificado=False))
    E.explicacion("Cada barra es una noticia (de la más antigua arriba a la más reciente abajo). El largo de la barra es el "
                  "<b>movimiento extra</b>: cuánto subió o bajó Nvidia por encima de lo que se esperaba dado lo que hizo el "
                  "mercado esos días. Naranja = restricción; azul = apertura. El asterisco (*) indica que el movimiento fue "
                  "tan grande que es poco probable que sea casualidad. Pasa el cursor sobre una barra para leer la noticia.",
                  "Casi todas las barras naranjas van a la izquierda (pérdida): en promedio, una restricción le quitó a Nvidia "
                  "3.5% extra en tres días. Las aperturas casi no la movieron. Además, las reacciones de 2022-2023 fueron las más "
                  "fuertes; las recientes son más chicas, porque el mercado ya espera estas noticias.")
    st.caption("Lo 'normal' se calcula con cómo se movió Nvidia frente al mercado en los 250 días hábiles anteriores a cada noticia. "
               "Fuente: precios de Yahoo Finance.")

    st.markdown("##### Ver una noticia de cerca")
    e_id = st.selectbox("Noticia", ev.id, format_func=lambda i: f"{i}: {ev.set_index('id').descripcion[i]}")
    fila = ev.set_index("id").loc[e_id]
    tr = A.trayectoria_evento(px, fila.fecha_reaccion, mercado)
    nombre_m = "S&P 500" if mercado == "SP500" else "SOX"
    f = go.Figure()
    f.add_trace(go.Scatter(x=tr.dia, y=tr.NVDA_pct, name="Nvidia: lo que realmente se movió", line=dict(color=E.AZUL)))
    f.add_trace(go.Scatter(x=tr.dia, y=tr.mercado_pct, name=f"{nombre_m}: lo que se movió el mercado", line=dict(color=E.GRIS)))
    f.add_trace(go.Scatter(x=tr.dia, y=tr.CAR_pct, name="Movimiento extra de Nvidia", line=dict(color=E.NARANJA, width=3)))
    f.add_vline(x=0, line=dict(color=E.GRIS, dash="dot"), annotation_text="día de la noticia")
    f.update_xaxes(title="Días antes (−) y después (+) de la noticia")
    f.update_yaxes(title="Cambio acumulado (%)")
    E.mostrar(E.fig(f, f"{e_id}, {fila.fecha_reaccion:%d-%m-%Y} ({fila.tipo.lower()}, medida de {fila.origen})", 400, leyenda=""))
    E.explicacion("Las tres líneas empiezan en cero 10 días antes de la noticia y van acumulando lo que pasó cada día. "
                  "La línea naranja es la que importa: lo que Nvidia se movió de más (o de menos) comparado con el mercado.",
                  "Si la línea naranja cae justo en el día 0, la noticia sí le pegó a Nvidia. Si se mueve antes, puede que la "
                  f"noticia ya se rumoraba. Fuente de la noticia: {fila.fuente}.")


def p3(D):
    q, an = D["q"], D["an"]
    E.pregunta("P3", T.PREGUNTAS["P3"])
    base = st.radio("Forma de contar las ventas por país", list(A.NOMBRE_BASE), format_func=lambda b: A.NOMBRE_BASE[b],
                    horizontal=True, key="p3base")
    s = q[q.base == base].melt(id_vars=["periodo"], value_vars=["eeuu", "taiwan", "china", "otros"], var_name="region", value_name="musd")
    s["region"] = s.region.map({"eeuu": "EE.UU.", "taiwan": "Taiwán", "china": "China", "otros": "Resto del mundo"})
    f = px_.bar(s, x="periodo", y="musd", color="region",
                color_discrete_map={"EE.UU.": E.AZUL, "China": E.NARANJA, "Taiwán": E.VERDE, "Resto del mundo": "#b9b8b2"},
                category_orders={"region": ["EE.UU.", "Taiwán", "Resto del mundo", "China"]},
                labels={"musd": "Ventas (millones de USD)", "periodo": "", "region": "País"})
    E.mostrar(E.fig(f, "El crecimiento vino de EE.UU.; China se volvió una franja delgada", 440, leyenda="País"))
    E.explicacion("Cada columna es un trimestre y su altura es todo lo que vendió Nvidia. Los colores muestran a qué país se vendió. "
                  "La franja naranja de arriba es China.",
                  "Las ventas totales se multiplicaron muchas veces, y casi todo ese crecimiento es azul (EE.UU.). "
                  "China no desapareció de golpe: se quedó del mismo tamaño mientras todo lo demás crecía, y desde 2025 se encogió.")

    anios = A.anios_disponibles(an, base)
    c1, c2 = st.columns(2)
    inicio = anios.index(2022) if 2022 in anios else 0
    y0 = c1.selectbox("Desde el año fiscal", anios[:-1], index=min(inicio, len(anios) - 2), key=f"y0{base}")
    hasta = [a for a in anios if a > y0]
    y1 = c2.selectbox("Hasta el año fiscal", hasta, index=len(hasta) - 1, key=f"y1{base}")
    dec = A.descomposicion(an, base, y0, y1)
    dec["region"] = dec.region.replace({"Otros": "Resto del mundo"})
    dec["sentido"] = dec.cambio_musd.map(lambda v: "Sumó ventas" if v >= 0 else "Restó ventas")
    f = px_.bar(dec, x="cambio_musd", y="region", orientation="h", color="sentido", text=dec.cambio_musd.map("{:+,.0f}".format),
                color_discrete_map={"Sumó ventas": E.AZUL, "Restó ventas": E.NARANJA},
                labels={"cambio_musd": "Cambio en ventas anuales (millones de USD)", "region": "", "sentido": ""})
    f.update_traces(textposition="outside")
    ch, us = dec.set_index("region").cambio_musd["China"], dec.set_index("region").cambio_musd["EE.UU."]
    E.mostrar(E.fig(f, f"FY{y0} a FY{y1}: China {ch:+,.0f} millones; EE.UU. {us:+,.0f} millones", 330, leyenda="", unificado=False))
    veces = f"EE.UU. sumó {abs(us/ch):,.0f} veces lo que China perdió." if ch < 0 else "En este periodo China todavía sumaba, sólo que mucho menos que EE.UU."
    E.explicacion("Cada barra dice cuántos millones de dólares más (azul) o menos (naranja) vendió Nvidia en ese país entre los "
                  "dos años elegidos. Puedes cambiar los años arriba.",
                  f"{veces} El problema ya no es China: ahora Nvidia depende muchísimo de EE.UU. (más de 60% de sus ventas) "
                  "y de unos pocos clientes grandes.")

    dc = an[["anio_fiscal", "total", "data_center"]].assign(pct_dc=lambda x: 100 * x.data_center / x.total)
    f = px_.line(dc, x="anio_fiscal", y="pct_dc", markers=True, color_discrete_sequence=[E.AZUL],
                 labels={"pct_dc": "% de las ventas que son chips para centros de datos", "anio_fiscal": "Año fiscal"})
    f.update_traces(marker=dict(size=9))
    f.update_yaxes(range=[0, 100])
    E.mostrar(E.fig(f, "Los chips para centros de datos (lo restringido) pasaron de 25% a 90% de las ventas", 320))
    E.explicacion("Cada punto es un año: qué parte de las ventas de Nvidia son chips para centros de datos (los de IA).",
                  "Nvidia se volvió casi 100% una empresa de chips de IA. Eso explica por qué las restricciones le importan "
                  "tanto: limitan justo su producto principal.")


def p4(D):
    px, an = D["px"], D["an"]
    E.pregunta("P4", T.PREGUNTAS["P4"])
    st.warning("Ojo: aquí mostramos cosas que pasaron **al mismo tiempo**. No prueba que las restricciones hayan causado "
               "el crecimiento de los competidores; también influyen los apoyos del gobierno chino y el auge de la IA.")
    idx = A.indice_rivales(D["riv"]).reset_index().melt(id_vars="anio", var_name="empresa", value_name="indice")
    f = px_.line(idx, x="anio", y="indice", color="empresa", markers=True,
                 color_discrete_map={"Cambricon": E.AZUL, "Hygon": E.NARANJA, "SMIC": E.VERDE},
                 labels={"indice": "Ventas (2022 = 100)", "anio": "", "empresa": "Competidor"})
    f.update_traces(marker=dict(size=9))
    f.add_hline(y=100, line=dict(color=E.GRIS, width=1), annotation_text="nivel de 2022")
    f.update_xaxes(dtick=1)
    E.mostrar(E.fig(f, "Cambricon multiplicó casi por 9 sus ventas entre 2022 y 2025", 400, leyenda="Competidor"))
    E.explicacion("Para comparar empresas de distinto tamaño y moneda, ponemos las ventas de 2022 en 100. Si una línea llega a 300, "
                  "esa empresa vende 3 veces lo que vendía en 2022.",
                  "Los tres competidores crecieron, y Cambricon (el que más se parece a Nvidia) se disparó en 2025, justo el año "
                  "en que Nvidia prácticamente dejó de vender chips de IA en China.")

    desde = st.date_input("Comparar el desempeño en bolsa a partir de", pd.Timestamp("2022-08-31"),
                          min_value=pd.Timestamp("2020-08-01"), max_value=px.index.max() - pd.Timedelta(days=30))
    rn = A.rend_normalizado(px, D["pxcn"], desde)
    sel = st.multiselect("Qué acciones mostrar", list(rn.columns), default=["NVDA", "SOX", "Cambricon", "Hygon"])
    rl = rn[sel].reset_index().melt(id_vars="fecha", var_name="serie", value_name="indice").dropna()
    f = px_.line(rl, x="fecha", y="indice", color="serie",
                 color_discrete_map={"NVDA": E.AZUL, "Cambricon": E.NARANJA, "SOX": E.VERDE, "Hygon": E.MORADO,
                                     "S&P 500": E.GRIS, "SMIC (Shanghái)": "#c2410c"},
                 labels={"indice": "Precio (fecha inicial = 100)", "fecha": "", "serie": "Acción o índice"})
    marcar_rondas(f, desde)
    E.mostrar(E.fig(f, "Desempeño en bolsa desde la fecha elegida", 460, leyenda="Acción o índice"))
    fin = (rn.ffill().iloc[-1] - 100)[sel]
    E.explicacion(f"Todas las líneas empiezan en 100 el {desde:%d-%m-%Y}. Si una línea llega a 500, quiere decir que la acción "
                  "vale 5 veces lo que valía ese día. Las líneas punteadas marcan las rondas de restricciones.",
                  "Ganancia acumulada al último día: " + ", ".join(f"{k} {v:+,.0f}%" for k, v in fin.items()) +
                  f". En este periodo, la que más subió fue {fin.idxmax()}. Desde ago-2022 a Nvidia le fue muy bien pese a China, "
                  "pero Cambricon subió todavía más: los inversionistas apostaron por el reemplazo local.")

    st.markdown("##### Comparación con ASML")
    cmp_ = D["asml"][["anio", "pct_china"]].rename(columns={"pct_china": "ASML"})
    nv = an[["anio_fiscal", "pct_china_facturacion", "pct_china_sede_cliente"]].copy()
    nv["anio"] = nv.anio_fiscal - 1
    cmp_ = cmp_.merge(nv.drop(columns="anio_fiscal"), on="anio", how="left").rename(
        columns={"pct_china_facturacion": "Nvidia (forma anterior)", "pct_china_sede_cliente": "Nvidia (forma nueva)"})
    cl = cmp_.melt(id_vars="anio", var_name="empresa", value_name="pct").dropna()
    f = px_.line(cl, x="anio", y="pct", color="empresa", markers=True,
                 color_discrete_map={"ASML": E.VERDE, "Nvidia (forma anterior)": E.AZUL, "Nvidia (forma nueva)": E.NARANJA},
                 labels={"pct": "% de las ventas que fueron a China", "anio": "Año", "empresa": "Empresa"})
    f.update_traces(marker=dict(size=9))
    f.update_xaxes(dtick=1)
    E.mostrar(E.fig(f, "Con reglas parecidas, China subió en ASML y bajó en Nvidia", 400, leyenda="Empresa"))
    E.explicacion("Cada punto es un año: qué parte de las ventas de cada empresa fue a China. ASML vende las máquinas para "
                  "fabricar chips y también tiene restricciones.",
                  "En ASML China <b>subió</b> hasta 36% en 2024 porque los clientes chinos compraron de más antes de que se "
                  "prohibieran las máquinas, y luego bajó. Lección: un salto repentino de China puede ser una señal de que "
                  "viene una restricción, no de un buen negocio duradero.")


def render(D):
    E.titulo("Fase 4 · Analizar: qué dicen los datos",
             "Una pestaña por pregunta. Debajo de cada gráfica explicamos cómo leerla y qué conclusión sacar.")
    tabs = st.tabs([f"{k}. {v['corto']}" for k, v in T.PREGUNTAS.items()])
    for t, fn in zip(tabs, [p1, p2, p3, p4]):
        with t:
            fn(D)
