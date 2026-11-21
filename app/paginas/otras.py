"""Páginas de texto: Inicio, Preguntar (Ask), Preparar (Prepare), Actuar (Act) y Glosario."""
import pandas as pd
import plotly.express as px_
import streamlit as st

import analisis as A
import estilos as E
import textos as T


def inicio(D):
    q, an = D["q"], D["an"]
    ult = q[q.base == "sede_cliente"].iloc[-1]
    E.titulo("Nvidia y China: ¿cómo manejar un mercado que se puede cerrar de un día para otro?",
             "Estudio de caso · Proyecto final de Ciencia de Datos · Datos públicos con corte al 20 de noviembre de 2026")
    st.markdown(f'<div class="nv-pregunta"><div class="nv-pq">La pregunta que respondemos</div>{T.PREGUNTA_CENTRAL}</div>',
                unsafe_allow_html=True)
    E.tarjetas([("China en las ventas de Nvidia (2022)", "26.4%", "una de cada cuatro dólares", "rosa", "🇨🇳"),
                (f"China en las ventas hoy ({ult.periodo})", f"{ult.pct_china:.1f}%", "menos de uno de cada diez", "rosa", "📉"),
                ("Ventas totales de Nvidia (FY2026)", f"{an.set_index('anio_fiscal').loc[2026, 'total']/1000:,.0f} mil MUSD", "8 veces más que en FY2023", "azul", "💵"),
                (f"EE.UU. en las ventas hoy ({ult.periodo})", f"{ult.pct_eeuu:.1f}%", "el nuevo riesgo", "azul", "🇺🇸")])
    E.seccion("Cómo está organizada esta app", "Sigue las 6 fases del estudio. Usa el menú de la izquierda.")
    E.pasos([("Preguntar", "Cuál es el problema, por qué pasa (5 porqués) y qué nos falta saber."),
             ("Preparar", "Qué datos usamos, de dónde vienen y qué tan confiables son."),
             ("Limpiar", "Cómo revisamos y arreglamos cada base, con gráficas del antes y después."),
             ("Analizar", "Las 4 preguntas respondidas con gráficas interactivas y su explicación."),
             ("Compartir", "Un tablero con lo más importante en una sola vista."),
             ("Actuar", "Qué recomendamos, cómo medirlo y en qué escenario estamos.")])
    E.seccion("Las 4 preguntas que guían el análisis")
    for k, p in T.PREGUNTAS.items():
        E.pregunta(k, p)
    st.info("¿No conoces algún término (H20, SOX, movimiento extra…)? Búscalo en el **Glosario** del menú.")


def ask(D):
    E.titulo("Fase 1 · Preguntar: ¿cuál es el problema?", "Antes de buscar datos, entendemos qué está pasando y qué necesitamos saber.")
    st.markdown(T.PROBLEMA)
    t1, t2, t3 = st.tabs(["Los 5 porqués", "Lo que nos falta (brechas)", "Las preguntas del estudio"])
    with t1:
        st.caption("Preguntamos '¿por qué?' cinco veces para llegar a la raíz del problema.")
        E.pasos(T.PORQUES)
        st.markdown(f'<div class="nv-explica"><b>Causa raíz:</b> {T.CAUSA_RAIZ}</div>', unsafe_allow_html=True)
    with t2:
        st.caption("Dónde estamos hoy, dónde deberíamos estar y cómo lo vamos a medir.")
        E.tabla(pd.DataFrame(T.BRECHAS, columns=["Tema", "Hoy", "Lo que debería pasar", "Cómo lo medimos"]))
    with t3:
        st.markdown(f"**Pregunta central:** {T.PREGUNTA_CENTRAL}")
        for k, p in T.PREGUNTAS.items():
            E.pregunta(k, p)
        st.markdown("**Qué estudiamos y qué no:** analizamos las ventas de Nvidia por país (2019 a mediados de 2026), el precio "
                    "de su acción y a tres competidores chinos que cotizan en bolsa, con ASML como comparación. No analizamos "
                    "la tecnología de los chips ni la política exterior en sí, sólo su efecto en ventas, en la acción y en los rivales.")


def prepare(D):
    E.titulo("Fase 2 · Preparar: ¿qué datos usamos?",
             "Siete bases de datos públicas. Aquí explicamos qué trae cada una, de dónde sale y qué tan confiable es.")
    tablas = {"nvda": D["q"], "px_us": D["px"].reset_index(), "px_cn": D["pxcn"].reset_index(), "eventos": D["ev"],
              "rivales": D["riv"], "asml": D["asml"], "sia": D["sia"]}
    filas = [{"Base": f'{T.BASES[k]["icono"]} {T.BASES[k]["nombre"]}', "Qué trae": T.BASES[k]["que_es"],
              "Fuente": T.BASES[k]["fuente"], "Filas": len(v), "Responde a": T.BASES[k]["preguntas"]} for k, v in tablas.items()]
    E.tabla(pd.DataFrame(filas), derecha=("Filas",))

    E.seccion("Explorar una base", "Elige una base para ver su descripción, qué significa cada columna y sus datos.")
    k = st.selectbox("Base", list(tablas), format_func=lambda x: f'{T.BASES[x]["icono"]} {T.BASES[x]["nombre"]}')
    info = T.BASES[k]
    st.markdown(f"**¿Qué hay aquí?** {info['que_es']}")
    E.tarjetas([("Fuente", info["fuente"], "", "blanco", "📂"), ("Periodo", info["periodo"], "", "blanco", "🗓️"),
                ("Tamaño", f"{len(tablas[k]):,} filas", f"{tablas[k].shape[1]} columnas", "blanco", "📏"),
                ("Confiabilidad", info["confianza"].split(":")[0], info["confianza"].split(":")[-1].strip() if ":" in info["confianza"] else "", "blanco", "✅")])
    c1, c2 = st.columns([2, 3])
    with c1:
        st.markdown("**¿Qué significa cada columna?**")
        E.tabla(pd.DataFrame(list(T.COLUMNAS[k].items()), columns=["Columna", "Qué significa"]), alto=360)
    with c2:
        st.markdown("**Los datos**")
        st.dataframe(tablas[k], width="stretch", height=360, hide_index=True)

    E.seccion("¿Qué tan buenas son las fuentes?",
              "Usamos la lista ROCCC: ¿es Confiable, Original, Completa, Actual y está Citada?")
    roccc = pd.DataFrame([
        ("Reportes de Nvidia y ASML a la SEC", "✅ Alta (auditados)", "✅ Fuente directa", "⚠️ Nvidia cambió el método en 2025", "✅ Hasta jul-2026", "✅"),
        ("Precios de Yahoo Finance", "✅ Alta", "⚠️ Reúne datos de las bolsas", "✅ Sin huecos", "✅ Hasta nov-2026", "✅"),
        ("Ventas de competidores (Yahoo)", "⚠️ Media", "⚠️ Secundaria", "⚠️ Sólo 4 años", "✅ 2025", "✅ Cotejada a mano"),
        ("Industria de chips (SIA)", "✅ Referencia del sector", "✅", "✅ Anual", "✅ 2025", "✅"),
        ("Prensa (noticias 2025-2026)", "⚠️ Media-alta", "⚠️ Secundaria", "✅", "✅", "✅"),
    ], columns=["Fuente", "Confiable", "Original", "Completa", "Actual", "Citada"])
    E.tabla(roccc)
    with st.expander("Limitaciones que hay que tener en cuenta"):
        st.markdown("""
- **Nvidia cambió en 2025 la forma de contar ventas por país.** Guardamos las dos series y nunca las mezclamos.
- **No sabemos a dónde llega el chip al final.** Nvidia reporta dónde está el cliente que compra, no dónde se usa el chip. Ventas a través de otros países (por ejemplo Singapur) o contrabando no se ven.
- **Huawei no cotiza en bolsa** y no publica cuánto vende de sus chips de IA, así que sólo lo mencionamos.
- **Los competidores reportan en yuanes y Nvidia en dólares:** comparamos cuánto crecieron, no cuánto venden.
- **Que dos cosas pasen al mismo tiempo no prueba que una cause la otra.**
- **Sólo usamos datos públicos**; no hay información personal ni confidencial.
""")


def act(D):
    q, px, ev = D["q"], D["px"], D["ev"]
    ult = q[q.base == "sede_cliente"].iloc[-1]
    E.titulo("Fase 6 · Actuar: ¿qué recomendamos?",
             "Lo que proponemos hacer, por qué, y cómo sabremos si está funcionando.")
    st.markdown(f'<div class="nv-pregunta"><div class="nv-pq">Nuestra respuesta en una frase</div>{T.RESPUESTA}</div>',
                unsafe_allow_html=True)
    st.caption("Importante: el efecto de estas recomendaciones es **esperado, no comprobado**, porque depende de decisiones "
               "de gobiernos que nadie controla. Es un ejercicio académico, no asesoría de inversión.")

    E.seccion("¿En qué escenario estamos hoy?",
              f"Con China en {ult.pct_china:.1f}% de las ventas en {ult.periodo}, marcamos el escenario que corresponde.")
    cols = st.columns(3)
    for c, (nom, disparador, (lo, hi), accion) in zip(cols, T.ESCENARIOS):
        actual = lo <= ult.pct_china < hi
        c.markdown(E.tarjeta(("👉 ESTAMOS AQUÍ · " if actual else "") + nom, f"China {lo}-{hi}%" if hi < 100 else f"China >{lo}%",
                             f"Qué tendría que pasar: {disparador}. Qué hacer: {accion}.",
                             "azul" if actual else "gris", ""), unsafe_allow_html=True)

    E.seccion("Tablero de seguimiento (KPIs)", "Indicadores para revisar cada trimestre: valor actual contra la meta que proponemos.")
    res = A.estudio_eventos(px, ev, "SP500", (-1, 1))
    riv = D["riv"].set_index(["empresa", "anio"]).crec_anual_pct
    fuera = 100 - ult.pct_eeuu - ult.pct_china
    kpis = pd.DataFrame([
        ("Ventas fuera de EE.UU. y China", f"{fuera:.1f}%", "Más de 30%", bool(fuera > 30), "Buscar otros mercados"),
        ("Peso de EE.UU. en las ventas", f"{ult.pct_eeuu:.1f}%", "Vigilar cada trimestre", None, "Vigilar la concentración"),
        ("Pérdidas por chips para China que no se vendieron", "4,900 millones (acumulado)", "0 por trimestre", False, "Fabricar sólo con doble permiso"),
        ("Golpe promedio de una mala noticia en la acción", f"{res[res.tipo=='Restricción'].CAR_pct.mean():+.1f}%", "Que la cartera pierda menos que eso", None, "Protegerse en fechas de riesgo"),
        ("Crecimiento de Cambricon", f"{riv[('Cambricon', 2025)]:+.0f}% (2025)", "Alerta si pasa de 50%", False, "Termómetro de competidores"),
        ("Crecimiento de Hygon", f"{riv[('Hygon', 2025)]:+.0f}% (2025)", "Alerta si pasa de 50%", False, "Termómetro de competidores"),
    ], columns=["Indicador", "Valor actual", "Meta propuesta", "ok", "Recomendación"])
    kpis["Estado"] = [E.badge("En meta", "verde") if o is True else E.badge("Fuera de meta / alerta", "rosa") if o is False
                      else E.badge("Seguimiento", "gris") for o in kpis.ok]
    E.tabla(kpis.drop(columns="ok"), html_cols=("Estado",))
    st.caption(f"Valores actuales calculados con los datos al {ult.periodo}. Las metas son propuestas del equipo.")

    t1, t2, t3 = st.tabs(["Para Nvidia", "Para el inversionista", "Lecciones del caso"])
    for t, lista in [(t1, T.RECOMENDACIONES_NVIDIA), (t2, T.RECOMENDACIONES_INVERSIONISTA)]:
        with t:
            for titulo_, que, porque, kpi, meta in lista:
                with st.container(border=True):
                    st.markdown(f"**{titulo_}**")
                    st.markdown(f"{que}")
                    st.markdown(f"<small>📊 <b>Lo que lo respalda:</b> {porque}<br>🎯 <b>Cómo medirlo:</b> {kpi} · "
                                f"<b>Meta:</b> {meta}</small>", unsafe_allow_html=True)
    with t3:
        E.pasos(T.LECCIONES)
        st.markdown("**¿Qué se pudo hacer mejor?** Planear desde el principio con el peor escenario, fabricar para China sólo "
                    "con permiso de ambos gobiernos, y medir cada trimestre cuánto se depende de China en dinero y en porcentaje.")


def glosario(D):
    E.titulo("Glosario", "Los términos técnicos del estudio explicados en palabras sencillas.")
    buscar = st.text_input("Buscar un término", placeholder="Ej.: H20, SOX, movimiento extra…").strip().lower()
    items = [(k, v) for k, v in T.GLOSARIO.items() if not buscar or buscar in k.lower() or buscar in v.lower()]
    if not items:
        st.info("No encontramos ese término.")
    for k, v in items:
        st.markdown(f"**{k}**  \n{v}")
