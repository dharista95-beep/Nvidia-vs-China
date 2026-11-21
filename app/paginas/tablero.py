"""Fase 5 · Compartir: tablero (dashboard) de una sola vista para la dirección e inversionistas."""
import pandas as pd
import plotly.express as px_
import streamlit as st

import analisis as A
import estilos as E
from paginas.analizar import lineas_por_base, marcar_rondas

HALLAZGOS = [
    ("China dejó de ser un motor de crecimiento.", "Su peso bajó con cada ronda de reglas: 25% → 20% → 12% → 6%."),
    ("Hasta 2025 fue 'dilución'; desde abril de 2025 es pérdida real.", "Antes China crecía menos que el resto; ahora vende 47% menos por trimestre."),
    ("La bolsa castiga las malas noticias y casi no premia las buenas.", "−3.5% extra en promedio con restricciones; +0.5% con aperturas."),
    ("EE.UU. tapó el hueco de China con creces, pero creó otra dependencia.", "En FY2026 EE.UU. sumó 13 veces lo que China restó; ya es más de 60% de las ventas."),
    ("Los competidores chinos crecieron justo cuando Nvidia salió.", "Cambricon vendió casi 9 veces más en 2025 que en 2022 (pasó al mismo tiempo; no está probada la causa)."),
]


def _mini(f, titulo, leyenda=None, alto=330):
    f = E.fig(f, titulo, alto, leyenda=leyenda)
    f.update_layout(title=dict(font=dict(size=14)), margin=dict(t=45, l=5, r=5, b=5))
    return f


def _llevarse(txt):
    st.markdown(f'<div class="nv-explica"><b>Para llevarse:</b> {txt}</div>', unsafe_allow_html=True)


def render(D):
    q, an, px, ev = D["q"], D["an"], D["px"], D["ev"]
    E.titulo("Fase 5 · Tablero para la dirección y los inversionistas",
             "Todo el estudio en una sola vista. Usa el filtro de fechas para enfocarte en un periodo.")
    st.markdown('<div class="nv-pregunta"><div class="nv-pq">Mensaje central</div>'
                'China ya no es un motor de crecimiento para Nvidia. Perderla le costó poco en ventas, pero cada noticia '
                'regulatoria sigue moviendo la acción, y ahora el riesgo está en depender demasiado de EE.UU.</div>',
                unsafe_allow_html=True)

    # Filtros en una sola fila
    c1, c2 = st.columns([3, 2])
    anios = c1.slider("Periodo", 2019, 2026, (2019, 2026))
    base = c2.radio("Forma de contar las ventas por país", list(A.NOMBRE_BASE), index=0, horizontal=True,
                    format_func=lambda b: {"facturacion": "Anterior (hasta 2025)", "sede_cliente": "Nueva (desde 2024)"}[b])
    d0, d1 = pd.Timestamp(f"{anios[0]}-01-01"), pd.Timestamp(f"{anios[1]}-12-31")

    # KPIs
    ult = q[q.base == "sede_cliente"].iloc[-1]
    res = A.estudio_eventos(px, ev, "SP500", (-1, 1))
    riv = D["riv"].set_index(["empresa", "anio"]).crec_anual_pct
    E.tarjetas([
        (f"China, % de ventas ({ult.periodo})", f"{ult.pct_china:.1f}%", "llegó a ser 28% en 2021", "rosa", "🇨🇳"),
        (f"EE.UU., % de ventas ({ult.periodo})", f"{ult.pct_eeuu:.1f}%", "el nuevo riesgo de concentración", "azul", "🇺🇸"),
        (f"Ventas del trimestre ({ult.periodo})", f"{ult.total/1000:,.1f} mil MUSD", f"vs. {q.set_index('periodo').total['FY2023-Q4']/1000:,.1f} mil MUSD a fines de 2022", "verde", "💵"),
        ("Golpe promedio de una mala noticia", f"{res[res.tipo=='Restricción'].CAR_pct.mean():+.1f}%", "movimiento extra de la acción en 3 días", "rosa", "📉"),
        ("Crecimiento de Cambricon (2025)", f"{riv[('Cambricon', 2025)]:+.0f}%", "el principal rival chino", "gris", "🏭"),
    ])

    # Fila 1
    g1, g2 = st.columns(2)
    with g1:
        s = q[(q.fin >= d0) & (q.fin <= d1)]
        f = marcar_rondas(lineas_por_base(s, "pct_china", [base]), d0)
        f.update_yaxes(title="% de las ventas", rangemode="tozero")
        E.mostrar(_mini(f, "1. Peso de China en las ventas de Nvidia", "Forma de contar"))
        _llevarse("cada ronda de reglas (líneas punteadas) bajó a China un escalón.")
    with g2:
        # Siempre el año clave: FY2025 a FY2026, cuando China cayó en dinero (forma de contar nueva)
        dec = A.descomposicion(an, "sede_cliente", 2025, 2026)
        dec["region"] = dec.region.replace({"Otros": "Resto del mundo"})
        dec["sentido"] = dec.cambio_musd.map(lambda v: "Sumó ventas" if v >= 0 else "Restó ventas")
        f = px_.bar(dec, x="cambio_musd", y="region", orientation="h", color="sentido",
                    text=dec.cambio_musd.map("{:+,.0f}".format),
                    color_discrete_map={"Sumó ventas": E.AZUL, "Restó ventas": E.NARANJA},
                    labels={"cambio_musd": "Cambio en ventas (millones de USD)", "region": "", "sentido": ""})
        f.update_traces(textposition="outside", cliponaxis=False)
        f.update_xaxes(range=[dec.cambio_musd.min() * 4, dec.cambio_musd.max() * 1.25])
        f.update_layout(hovermode="closest")
        E.mostrar(_mini(f, "2. Quién sumó y quién restó ventas en el último año (FY2025 a FY2026)", ""))
        ch, us = dec.set_index("region").cambio_musd["China"], dec.set_index("region").cambio_musd["EE.UU."]
        _llevarse(f"China restó {abs(ch):,.0f} millones, pero EE.UU. sumó {us:,.0f}: {us/abs(ch):,.0f} veces más.")

    # Fila 2
    g3, g4 = st.columns(2)
    with g3:
        e = res[(pd.to_datetime(res.fecha) >= d0) & (pd.to_datetime(res.fecha) <= d1)].copy()
        e["etiqueta"] = e.id + " " + pd.to_datetime(e.fecha).dt.strftime("%m/%Y")
        f = px_.bar(e.iloc[::-1], x="CAR_pct", y="etiqueta", color="tipo", orientation="h",
                    color_discrete_map={"Restricción": E.NARANJA, "Apertura": E.AZUL},
                    hover_data={"descripcion": True, "etiqueta": False},
                    labels={"CAR_pct": "Movimiento extra de la acción (%)", "etiqueta": "", "tipo": "Noticia"})
        f.update_yaxes(categoryorder="array", categoryarray=list(e.etiqueta[::-1]))
        f.update_layout(hovermode="closest")
        E.mostrar(_mini(f, "3. Reacción de la acción a cada noticia", "Noticia", 360))
        _llevarse("las restricciones (naranja) le quitan valor a la acción; las aperturas (azul) casi no le suman.")
    with g4:
        rn = A.rend_normalizado(px, D["pxcn"], max(d0, pd.Timestamp("2020-08-01")))
        rn = rn[rn.index <= d1][["NVDA", "SOX", "Cambricon"]]
        rl = rn.reset_index().melt(id_vars="fecha", var_name="serie", value_name="indice").dropna()
        f = px_.line(rl, x="fecha", y="indice", color="serie",
                     color_discrete_map={"NVDA": E.AZUL, "Cambricon": E.NARANJA, "SOX": E.VERDE},
                     labels={"indice": "Precio (inicio del periodo = 100)", "fecha": "", "serie": "Acción"})
        E.mostrar(_mini(f, "4. Nvidia vs. su principal rival chino en bolsa", "Acción", 360))
        fin = (rn.ffill().iloc[-1] - 100).round(0)
        _llevarse(f"en este periodo NVDA {fin['NVDA']:+,.0f}%, Cambricon {fin['Cambricon']:+,.0f}% y el sector (SOX) "
                  f"{fin['SOX']:+,.0f}%. Desde la primera restricción (ago-2022), Cambricon subió más que Nvidia.")

    E.seccion("Los 5 hallazgos clave")
    for i, (t, d) in enumerate(HALLAZGOS, 1):
        st.markdown(f'<div class="nv-paso"><div class="nv-num">{i}</div><div class="nv-paso-txt"><b>{t}</b>{d}</div></div>',
                    unsafe_allow_html=True)

    with st.expander("Ver las figuras del documento final (PDF)"):
        figs = {"Peso de China": "fig1_peso_china_trimestral.png", "Crecimiento por región": "fig2_descomposicion_regiones.png",
                "Reacción de la acción": "fig3_estudio_eventos.png", "Rivales chinos": "fig4_rivales_chinos.png",
                "ASML vs. Nvidia": "fig5_asml_vs_nvidia.png"}
        for t, (nombre, archivo) in zip(st.tabs(list(figs)), figs.items()):
            with t:
                st.image(str(A.FIG / archivo), width="stretch")
