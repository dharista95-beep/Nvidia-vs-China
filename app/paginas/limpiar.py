"""Fase 3 · Limpiar (Process).

Para cada base: qué hay, revisión de calidad, repetidos, reglas de validación,
decisiones de limpieza (con su razón) y comparación entre la base original y
la base limpia. Las bases originales (data/raw) nunca se modifican.
"""
import numpy as np
import pandas as pd
import plotly.express as px_
import plotly.graph_objects as go
import streamlit as st

import analisis as A
import estilos as E
import textos as T


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def _regla(nombre, que_revisa, n_falla):
    return {"Regla": nombre, "¿Qué revisa y por qué?": que_revisa, "Casos que no cumplen": int(n_falla),
            "Resultado": "Cumple" if n_falla == 0 else "Revisar"}


def _metricas(df, fecha=None):
    m = {"Filas": len(df), "Columnas": df.shape[1], "Celdas vacías": int(df.isna().sum().sum()),
         "Filas repetidas exactas": int(df.duplicated().sum())}
    if fecha is not None and fecha in df:
        f = pd.to_datetime(df[fecha])
        m["Periodo cubierto"] = f"{f.min():%d-%m-%Y} a {f.max():%d-%m-%Y}"
    return m


# ---------------------------------------------------------------------------
# Definición de cada base: original, limpia, reglas, decisiones y gráfica
# ---------------------------------------------------------------------------
def base_nvda(D, R):
    xb, q, lg, an = R["xbrl"], D["q"], D["largo"], D["an"]
    conservadas = xb[xb.dims.isin(A.MAPA_XBRL)]
    repetidos = int(xb.duplicated(["inicio", "fin", "dims"]).sum())
    derivados = int((lg.origen != "reportado").sum())
    v = A.validaciones(D).set_index("id").ok
    reglas = [
        _regla("Las regiones no suman más que el total", "Si EE.UU. + Taiwán + China pasaran del total, habría un dato mal leído.", (q.otros < -1).sum()),
        _regla("El 4.º trimestre calculado no sale negativo", "Ese trimestre lo calculamos nosotros; un negativo indicaría que restamos mal.", (lg[lg.origen != "reportado"].valor_musd < 0).sum()),
        _regla("Los 4 trimestres suman el total del año", "Comprueba que nuestros trimestres cuadran con el reporte anual oficial.", 0 if v["V3"] else 1),
        _regla("Centros de datos no es mayor que el total", "Una parte no puede ser más grande que el todo.", (q.data_center > q.total).sum()),
        _regla("No falta ningún trimestre", "Deben estar los 24 trimestres seguidos en la forma de contar anterior, sin huecos ni repetidos.", 0 if v["V5"] else 1),
        _regla("Cuadra con el reporte anual 2026", "Cotejo a mano: China 19,677 y total 215,938 millones, como dice el texto del 10-K.", 0 if v["V6"] else 1),
        _regla("Los porcentajes están entre 0 y 100", "Un porcentaje fuera de ese rango indicaría una división mal hecha.", ((q[["pct_china", "pct_eeuu", "pct_dc"]] < 0) | (q[["pct_china", "pct_eeuu", "pct_dc"]] > 100)).sum().sum()),
    ]
    decisiones = [
        ("Quedarnos sólo con lo que responde las preguntas", "Los reportes traen las ventas cortadas de 26 formas. Usamos total, EE.UU., Taiwán, China, centros de datos y videojuegos (D-03).",
         f"{len(xb):,} → {len(conservadas):,} datos"),
        ("Unir las dos etiquetas de China", "Hasta 2022 China venía como 'CN' y después como 'China incluyendo Hong Kong'. En los años que aparecen las dos, las cifras son idénticas (D-04).", "1 sola variable 'china'"),
        ("Si un dato aparece en varios reportes, usar el más reciente", "Cada trimestre se repite en reportes posteriores; el último trae las correcciones (D-06).",
         f"{repetidos:,} repeticiones eliminadas"),
        ("Calcular el 4.º trimestre", "Nvidia no publica reporte del 4.º trimestre; se calcula como total del año menos los primeros 9 meses (D-07).",
         f"{derivados} datos calculados"),
        ("No mezclar las dos formas de contar ventas por país", "En oct-2025 Nvidia cambió el método y China pesa más con el nuevo. Unirlas crearía un salto que no existió (D-05).",
         "2 series separadas"),
        ("Dejar vacío 'videojuegos' en los dos trimestres de FY2027", "Ese dato no viene en los reportes de 2026 en el formato que usamos; preferimos dejarlo vacío que inventarlo.", "2 celdas vacías"),
        ("'Otros países' = total menos los tres países", "Los nombres del resto del mundo cambiaron con los años (Europa, Singapur, etc.) (D-08).", "Columna 'otros'"),
    ]
    return dict(original=xb, limpia=q, fecha=None, reglas=reglas, decisiones=decisiones,
                repetidos=(repetidos, "veces que el mismo dato (mismo periodo y mismo corte) aparece en más de un reporte"),
                grafica=lambda: _graf_nvda(xb, conservadas, lg, q))


def _graf_nvda(xb, conservadas, lg, q):
    etapas = pd.DataFrame({"Etapa": ["Datos extraídos de 24 reportes", "Sólo los cortes que usamos",
                                     "Sin repetidos (un dato por trimestre)", "Tabla final (filas = trimestres)"],
                           "Cantidad": [len(xb), len(conservadas), len(lg), len(q)]})
    f = px_.funnel(etapas, x="Cantidad", y="Etapa", color_discrete_sequence=[E.AZUL])
    f.update_yaxes(title=None)
    E.mostrar(E.fig(f, "De 1,122 datos sueltos a una tabla de 32 trimestres", 330, unificado=False))
    E.explicacion("Cada barra es un paso de la limpieza; el número dice cuántos datos quedan después de ese paso.",
                  "La mayoría de lo que se descarta no es 'basura': son cortes que no usamos (por ejemplo, ventas de autos) "
                  "o el mismo dato repetido en varios reportes. Nada se inventa ni se borra a mano.")

    unir = st.toggle("¿Qué pasaría si uniéramos las dos formas de contar?", value=False)
    f = go.Figure()
    if unir:
        s = q.sort_values(["fin", "base"]).drop_duplicates("fin", keep="last")
        f.add_trace(go.Scatter(x=s.fin, y=s.pct_china, name="Serie unida (incorrecta)", mode="lines+markers",
                               line=dict(color=E.GRIS, width=2), marker=dict(size=8)))
    else:
        for b, col, dash in [("facturacion", E.AZUL, "solid"), ("sede_cliente", E.NARANJA, "dash")]:
            s = q[q.base == b]
            f.add_trace(go.Scatter(x=s.fin, y=s.pct_china, name=A.NOMBRE_BASE[b], mode="lines+markers",
                                   line=dict(color=col, dash=dash, width=2), marker=dict(size=8)))
    f.update_yaxes(title="% de las ventas que fueron a China", rangemode="tozero")
    E.mostrar(E.fig(f, "Por qué guardamos dos series de China y no una", 400, leyenda="Forma de contar"))
    E.explicacion("Cada punto es un trimestre. Línea azul: método anterior (según dónde se facturaba). "
                  "Línea naranja punteada: método nuevo (según dónde está la oficina central del cliente). "
                  "Activa el botón de arriba para ver qué pasaría si las pegáramos en una sola línea.",
                  "En los trimestres donde existen las dos, el método nuevo le da a China entre 3 y 9 puntos más. "
                  "Si las uniéramos, parecería que China saltó de 12% a 23% a finales de 2024, y eso nunca pasó. Por eso se analizan por separado.")


def base_px_us(D, R):
    raw = R["px_us"]
    limpia = D["px"].reset_index()
    precios = limpia[["NVDA", "AMD", "ASML", "SP500", "SOX"]]
    r = limpia.filter(like="r_").dropna()
    reglas = [
        _regla("No hay días sin precio", "Un hueco movería los cálculos de rendimiento.", precios.isna().sum().sum()),
        _regla("Ninguna fecha está repetida", "Cada día debe aparecer una sola vez.", limpia.fecha.duplicated().sum()),
        _regla("Las fechas van en orden", "Para calcular el cambio de un día a otro, deben estar ordenadas.", int(not limpia.fecha.is_monotonic_increasing)),
        _regla("Todos los precios son mayores que cero", "Un precio en cero o negativo sería un error.", (precios <= 0).sum().sum()),
        _regla("Ningún día sube o baja más de 50%", "Si un 'split' no estuviera ajustado, veríamos una caída falsa de 75% o 90% en un día.", (r.abs() >= 0.5).sum().sum()),
    ]
    decisiones = [
        ("Usar el precio ajustado", "Nvidia dividió sus acciones 4 a 1 (2021) y 10 a 1 (2024). Sin ajustar, parecería que la acción se desplomó esos días (D-09).", "Sin saltos falsos"),
        ("Ponerle nombre claro a los índices", "Yahoo los llama ^GSPC y ^SOX; los renombramos a SP500 y SOX.", "2 columnas renombradas"),
        ("Calcular cuánto se movió cada día", "Es lo que necesita el estudio de la reacción a noticias (D-12).", "5 columnas nuevas (r_*)"),
        ("Quitar días con algún precio faltante", "Para que todas las series tengan los mismos días (D-12). No hubo ninguno.", "0 días quitados"),
    ]
    return dict(original=raw, limpia=limpia, fecha="fecha", reglas=reglas, decisiones=decisiones,
                repetidos=(int(raw.Date.duplicated().sum()), "fechas repetidas"),
                grafica=lambda: _graf_px_us(limpia))


def _graf_px_us(limpia):
    r = (limpia[["fecha", "r_NVDA"]].dropna().assign(mov=lambda x: 100 * (np.exp(x.r_NVDA) - 1)))
    f = px_.histogram(r, x="mov", nbins=100, color_discrete_sequence=[E.AZUL],
                      labels={"mov": "Cuánto subió o bajó NVDA en un día (%)", "count": "Número de días"})
    for v in (-50, 50):
        f.add_vline(x=v, line=dict(color=E.NARANJA, dash="dash"), annotation_text="límite ±50%")
    f.update_xaxes(range=[-60, 60])
    f.update_yaxes(title="Número de días")
    E.mostrar(E.fig(f, f"Ningún día pasó de ±50%: el peor fue {r.mov.min():.1f}% y el mejor +{r.mov.max():.1f}%", 380, unificado=False))
    E.explicacion("Cada barra cuenta cuántos días la acción de Nvidia se movió en ese rango. Las líneas naranjas marcan el "
                  "límite de ±50% que usamos como alarma.",
                  "Casi todos los días se mueve entre −5% y +5%. Como ningún día llega al límite, sabemos que los 'splits' "
                  "ya están bien ajustados y los precios se pueden comparar en el tiempo.")


def base_px_cn(D, R):
    raw = R["px_cn"]
    limpia = D["pxcn"].reset_index()
    nombres = {"688041.SS": "Hygon", "688256.SS": "Cambricon", "688981.SS": "SMIC"}
    vacios_despues = sum(int(raw[c][raw.index >= raw[c].first_valid_index()].isna().sum()) for c in nombres)
    reglas = [
        _regla("Los únicos vacíos son de antes de salir a bolsa", "Hygon empezó a cotizar en ago-2022 y Cambricon en jul-2020; antes no existe precio.", vacios_despues),
        _regla("Ninguna fecha está repetida", "Cada día debe aparecer una sola vez.", raw.Date.duplicated().sum()),
        _regla("Todos los precios son mayores que cero", "Un precio en cero o negativo sería un error.", (raw[list(nombres)] <= 0).sum().sum()),
    ]
    decisiones = [
        ("Guardarlos en un archivo aparte", "La bolsa de Shanghái abre otros días que la de EE.UU. y cotiza en yuanes. Juntarlos crearía huecos artificiales (D-11).", "1 archivo propio"),
        ("No rellenar los vacíos", "Antes de salir a bolsa no hay precio; inventarlo sería falso.", f"{int(raw.isna().sum().sum())} celdas vacías se quedan así"),
        ("Comparar con índice base 100, no en dinero", "Están en yuanes y Nvidia en dólares; se compara cuánto crecieron, no cuánto valen.", "Ver P4"),
    ]
    return dict(original=raw, limpia=limpia, fecha="fecha", reglas=reglas, decisiones=decisiones,
                repetidos=(int(raw.Date.duplicated().sum()), "fechas repetidas"),
                grafica=lambda: _graf_px_cn(raw, nombres))


def _graf_px_cn(raw, nombres):
    pc = raw.set_index(pd.to_datetime(raw.Date)).drop(columns="Date").rename(columns=nombres)
    mapa = pc.notna().resample("QE").mean().T * 100
    mapa.columns = [f"{c.year}-T{c.quarter}" for c in mapa.columns]
    f = px_.imshow(mapa, aspect="auto", color_continuous_scale=["#FDF0F4", E.AZUL], zmin=0, zmax=100,
                   labels=dict(color="% de días con precio", x="Trimestre", y="Empresa"))
    E.mostrar(E.fig(f, "Los vacíos son sólo de Hygon antes de salir a bolsa (ago-2022)", 280, unificado=False))
    E.explicacion("Cada cuadro es un trimestre para una empresa. Azul fuerte = hay precio todos los días; "
                  "rosa = no hay precio.",
                  "Los huecos están todos al inicio de Hygon (y dos días de Cambricon), justo antes de que empezaran a "
                  "cotizar. No es un error de los datos, así que no se rellenan.")


def base_eventos(D, R):
    ev = D["ev"]
    px = D["px"]
    dias = (ev.fecha_reaccion - ev.fecha_anuncio).dt.days
    reglas = [
        _regla("Cada evento tiene una clave única", "Para no contar dos veces la misma noticia.", ev.id.duplicated().sum()),
        _regla("La reacción no es antes del anuncio", "La bolsa no puede reaccionar a algo que no se ha dicho.", (dias < 0).sum()),
        _regla("La reacción es un día con bolsa abierta", "Si cayera en fin de semana o feriado, no habría precio para medir.", (~ev.fecha_reaccion.isin(px.index)).sum()),
        _regla("El origen es EE.UU. o China", "Sólo estudiamos medidas de esos dos gobiernos.", (~ev.origen.isin(["EE.UU.", "China"])).sum()),
        _regla("Cada evento tiene su fuente", "Sin fuente no se puede verificar.", ev.fuente.isna().sum()),
        _regla("Hay al menos 250 días de historia antes", "Se necesitan para saber cómo se mueve 'normalmente' la acción.", (px.index.get_indexer(ev.fecha_reaccion) < 250).sum()),
    ]
    decisiones = [
        ("Usar el primer día en que la bolsa pudo reaccionar", "Si la noticia salió con la bolsa cerrada, el efecto se ve al día siguiente (D-13).",
         f"{int((dias > 0).sum())} fechas movidas un día"),
        ("Clasificar cada noticia como restricción o apertura", "Para comparar cómo reacciona la acción a malas y buenas noticias (A-05).",
         f"{int((ev.tipo == 'Restricción').sum())} restricciones y {int((ev.tipo == 'Apertura').sum())} aperturas"),
        ("Cruzar fechas de prensa con reportes de Nvidia", "La prensa a veces se adelanta o se equivoca; cuando fue posible, se confirmó con la SEC.", "12 eventos con fuente"),
    ]
    return dict(original=ev.drop(columns=["tipo"]), limpia=ev, fecha="fecha_reaccion", reglas=reglas,
                decisiones=decisiones, repetidos=(int(ev.id.duplicated().sum()), "eventos repetidos"),
                grafica=lambda: _graf_eventos(ev))


def _graf_eventos(ev):
    d = ev.assign(y=ev.origen.map({"EE.UU.": "Medida de EE.UU.", "China": "Medida de China"}),
                  texto=ev.id)
    f = px_.scatter(d, x="fecha_reaccion", y="y", color="tipo", text="texto", hover_data={"descripcion": True, "texto": False, "y": False},
                    color_discrete_map={"Restricción": E.NARANJA, "Apertura": E.AZUL},
                    labels={"fecha_reaccion": "", "y": "", "tipo": "Tipo de noticia"})
    f.update_traces(marker=dict(size=16, line=dict(color="white", width=2)), textposition="top center")
    E.mostrar(E.fig(f, "12 noticias en 4 años, y desde 2025 cada vez más seguidas", 300, leyenda="Tipo de noticia", unificado=False))
    E.explicacion("Cada punto es una noticia. Naranja = restricción (malo para Nvidia); azul = apertura (bueno). "
                  "Arriba o abajo según qué gobierno la tomó. Pasa el cursor sobre un punto para leer qué pasó.",
                  "Hasta 2024 las noticias venían de EE.UU. y espaciadas. Desde 2025 son más frecuentes y China también "
                  "empezó a poner trabas: el entorno se volvió más impredecible.")


def base_rivales(D, R):
    rv = D["riv"]
    recalculado = rv.groupby("empresa").ingresos_millones.pct_change() * 100
    reglas = [
        _regla("Cada empresa tiene sus 4 años (2022-2025)", "Para comparar el mismo periodo en las tres.", int((rv.groupby("empresa").anio.count() != 4).sum())),
        _regla("Las ventas son mayores que cero", "Unas ventas en cero o negativas serían un error.", (rv.ingresos_millones <= 0).sum()),
        _regla("La moneda es CNY o USD", "Hay que saber en qué moneda está cada cifra.", (~rv.moneda.isin(["CNY", "USD"])).sum()),
        _regla("El crecimiento está bien calculado", "Se recalcula y se compara con la columna guardada.", int(((recalculado - rv.crec_anual_pct).abs() > 0.01).sum())),
        _regla("SMIC cuadra con su reporte anual", "Cotejo a mano: ventas 2024 de 8,030 millones de dólares.",
               int(abs(rv[(rv.empresa == "SMIC") & (rv.anio == 2024)].ingresos_millones.iloc[0] - 8030) > 1)),
    ]
    decisiones = [
        ("Corregir la moneda de SMIC", "Yahoo la marcaba en yuanes, pero SMIC reporta en dólares. Lo descubrimos al cotejar con su reporte anual (D-14).", "1 empresa corregida"),
        ("Comparar con índice 2022 = 100", "Las monedas son distintas y sólo hay 4 años; comparamos cuánto crecieron, no los montos (A-08).", "Ver P4"),
        ("Dejar vacío el crecimiento de 2022", "No hay año anterior en la base para calcularlo.", "3 celdas vacías"),
    ]
    return dict(original=rv, limpia=rv, fecha=None, reglas=reglas, decisiones=decisiones,
                repetidos=(int(rv.duplicated(["empresa", "anio"]).sum()), "empresa-año repetidos"),
                grafica=lambda: _graf_rivales(rv))


def _graf_rivales(rv):
    d = rv.assign(etiqueta=rv.empresa + " (" + rv.moneda + ")")
    f = px_.bar(d, x="anio", y="ingresos_millones", color="empresa", facet_col="etiqueta",
                color_discrete_map={"Cambricon": E.AZUL, "Hygon": E.NARANJA, "SMIC": E.VERDE},
                labels={"ingresos_millones": "Ventas (millones)", "anio": "", "etiqueta": "", "empresa": "Empresa"})
    f.update_yaxes(matches=None, showticklabels=True)
    f.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    E.mostrar(E.fig(f, "Ventas anuales de cada competidor, en su propia moneda", 340, leyenda="Empresa", unificado=False))
    E.explicacion("Una gráfica por empresa, cada una con su propia escala y su moneda entre paréntesis. "
                  "Por eso no se deben comparar las alturas entre gráficas, sólo la tendencia de cada una.",
                  "Las tres crecen, pero Cambricon da un salto enorme en 2025. La limpieza importante fue la moneda de SMIC: "
                  "sin corregirla, sus ventas se habrían leído como 7 veces más chicas.")


def base_asml(D, R):
    a = D["asml"]
    reglas = [
        _regla("China no es mayor que el total", "Una parte no puede ser más grande que el todo.", (a.china_meur > a.total_meur).sum()),
        _regla("El porcentaje está bien calculado", "Se recalcula China ÷ total × 100.", int(((100 * a.china_meur / a.total_meur - a.pct_china).abs() > 0.01).sum())),
        _regla("No falta ningún año", "Deben estar todos los años de 2017 a 2025.", int(a.anio.max() - a.anio.min() + 1 - a.anio.nunique())),
    ]
    decisiones = [
        ("Usar sólo datos anuales", "Es un recuadro de comparación; los datos por trimestre sólo vienen en comunicados sin formato (D-16).", "9 años"),
        ("Usar el reporte más reciente si un año se repite", "El último reporte trae las correcciones (D-06).", "1 dato por año"),
    ]
    return dict(original=a, limpia=a, fecha=None, reglas=reglas, decisiones=decisiones,
                repetidos=(int(a.anio.duplicated().sum()), "años repetidos"), grafica=lambda: _graf_asml(a))


def _graf_asml(a):
    f = px_.bar(a, x="anio", y="pct_china", text=a.pct_china.map("{:.0f}%".format), color_discrete_sequence=[E.VERDE],
                labels={"pct_china": "% de las ventas de ASML que fueron a China", "anio": ""})
    E.mostrar(E.fig(f, "En ASML, China subió hasta 36% en 2024", 320, unificado=False))
    E.explicacion("Cada barra es un año: qué parte de lo que vendió ASML fue a China.",
                  "Al revés que Nvidia, en ASML China subió con las restricciones: los clientes chinos compraron máquinas "
                  "de más antes de que se prohibieran.")


def base_sia(D, R):
    s = D["sia"]
    reglas = [
        _regla("No falta ningún año", "Deben estar todos los años de 2019 a 2025.", int(s.anio.max() - s.anio.min() + 1 - s.anio.nunique())),
        _regla("Las ventas son mayores que cero", "Una venta en cero sería un error de captura.", (s.ventas_globales_musd <= 0).sum()),
        _regla("Cada cifra tiene su fuente", "Se capturaron a mano; cada una dice de qué comunicado salió.", s.fuente.isna().sum()),
    ]
    decisiones = [
        ("Capturar las cifras a mano", "La SIA no tiene descarga automática; son sólo 7 números de sus comunicados anuales (D-15).", "7 cifras"),
        ("Comparar con el año fiscal anterior de Nvidia", "El año de Nvidia termina en enero, casi igual que el año calendario anterior (A-07).", "Ver P3"),
    ]
    return dict(original=s, limpia=s, fecha=None, reglas=reglas, decisiones=decisiones,
                repetidos=(int(s.anio.duplicated().sum()), "años repetidos"), grafica=lambda: _graf_sia(s))


def _graf_sia(s):
    f = px_.bar(s, x="anio", y=s.ventas_globales_musd / 1000, color_discrete_sequence=[E.GRIS],
                labels={"y": "Ventas mundiales de chips (miles de millones de USD)", "anio": ""})
    f.update_yaxes(title="Miles de millones de USD")
    E.mostrar(E.fig(f, "La industria de chips creció 92% de 2019 a 2025", 320, unificado=False))
    E.explicacion("Cada barra es lo que vendió toda la industria de chips en el mundo ese año.",
                  "Sirve de referencia: Nvidia creció mucho más rápido que la industria, así que ganó participación.")


BASES = {"nvda": base_nvda, "px_us": base_px_us, "px_cn": base_px_cn, "eventos": base_eventos,
         "rivales": base_rivales, "asml": base_asml, "sia": base_sia}


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
def render(D, R):
    E.titulo("Fase 3 · Limpiar los datos",
             "Revisamos cada base: qué trae, qué le falta, qué se repite y si los números cuadran. "
             "Luego explicamos cada cambio que hicimos y por qué. Los archivos originales nunca se tocan.")

    defs = {k: f(D, R) for k, f in BASES.items()}

    E.seccion("Resumen: qué revisamos en cada base",
              "Cada base pasa por reglas distintas según lo que contiene. Abajo puedes ver el detalle de cada una.")
    filas = []
    for k, d in defs.items():
        ok = sum(r["Resultado"] == "Cumple" for r in d["reglas"])
        filas.append({"Base": f'{T.BASES[k]["icono"]} {T.BASES[k]["nombre"]}',
                      "Reglas revisadas": len(d["reglas"]),
                      "Resultado": E.badge(f"{ok} de {len(d['reglas'])} cumplen", "verde" if ok == len(d["reglas"]) else "rosa"),
                      "Limpieza principal": d["decisiones"][0][0]})
    E.tabla(pd.DataFrame(filas), html_cols=("Resultado",), derecha=("Reglas revisadas",))

    k = st.radio("Elige la base que quieres ver", list(defs), horizontal=True,
                 format_func=lambda x: f'{T.BASES[x]["icono"]} {T.BASES[x]["nombre"]}')
    d, info = defs[k], T.BASES[k]

    # 0. Qué hay
    E.seccion(f"{info['icono']} {info['nombre']}", info["que_es"])
    E.tarjetas([("De dónde viene", info["fuente"], "", "blanco", "📂"),
                ("Qué periodo cubre", info["periodo"], "", "blanco", "🗓️"),
                ("Para qué pregunta sirve", info["preguntas"], "", "blanco", "❓"),
                ("Qué tan confiable es", info["confianza"].split(":")[0], info["confianza"].split(":")[-1].strip()
                 if ":" in info["confianza"] else "", "blanco", "✅")])
    with st.expander("¿Qué significa cada columna?"):
        E.tabla(pd.DataFrame(list(T.COLUMNAS[k].items()), columns=["Columna", "Qué significa"]))

    # 1. Revisión de calidad
    o, l = d["original"], d["limpia"]
    E.seccion("1. Revisión de calidad", "Qué falta y qué se repite en la base original, antes de tocar nada.")
    vacias = int(o.isna().sum().sum())
    rep_n, rep_txt = d["repetidos"]
    E.tarjetas([("Filas en la base original", f"{len(o):,}", f"{o.shape[1]} columnas", "azul", "📄"),
                ("Celdas vacías", f"{vacias:,}", f"de {o.size:,} celdas", "rosa" if vacias else "gris", "🕳️"),
                ("Filas idénticas repetidas", f"{int(o.duplicated().sum())}", "copias exactas", "gris", "📑"),
                ("Datos repetidos", f"{rep_n:,}", rep_txt, "rosa" if rep_n else "gris", "🔁")])
    if vacias:
        na = o.isna().sum()
        na = na[na > 0].rename("Celdas vacías").reset_index().rename(columns={"index": "Columna"})
        na["% de la columna"] = (100 * na["Celdas vacías"] / len(o)).map("{:.1f}%".format)
        E.tabla(na, derecha=("Celdas vacías", "% de la columna"), alto=200)

    # 2. Reglas
    E.seccion("2. Reglas de validación", "Pruebas automáticas que se recalculan cada vez que abres la app. Sólo revisan; no cambian nada.")
    rg = pd.DataFrame(d["reglas"])
    rg["Resultado"] = [E.badge(x, "verde" if x == "Cumple" else "rosa") for x in rg.Resultado]
    E.tabla(rg, html_cols=("Resultado",), derecha=("Casos que no cumplen",))

    # 3. Decisiones
    E.seccion("3. Decisiones de limpieza", "Lo que cambiamos, por qué y qué efecto tuvo. La clave entre paréntesis remite a la bitácora del documento.")
    E.tabla(pd.DataFrame(d["decisiones"], columns=["Qué hicimos", "Por qué", "Efecto"]))

    # 4. Antes vs después
    E.seccion("4. Base original vs. base limpia")
    mo, ml = _metricas(o, d["fecha"] if d["fecha"] in o else None), _metricas(l, d["fecha"])
    comp = pd.DataFrame({"Medida": list(ml), "Original": [mo.get(m, "—") for m in ml], "Limpia": list(ml.values())})
    comp["Limpia"] = [E.badge(n, "rosa") if str(n) != str(o_) else str(n) for o_, n in zip(comp.Original, comp.Limpia)]
    comp["Original"] = comp.Original.astype(str)
    E.tabla(comp, html_cols=("Limpia",), derecha=("Original", "Limpia"))
    st.caption("En rosa, lo que cambió con la limpieza.")
    c1, c2 = st.columns(2)
    with c1.expander("Ver la base original (primeras 50 filas)"):
        st.dataframe(o.head(50), width="stretch", hide_index=True)
    with c2.expander("Ver la base limpia (primeras 50 filas)"):
        st.dataframe(l.head(50), width="stretch", hide_index=True)
    st.download_button("Descargar la base limpia (CSV)", l.to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"{k}_limpia.csv", mime="text/csv")

    # 5. Visualización
    E.seccion("5. Visualizar la limpieza")
    d["grafica"]()

    with st.expander("Bitácora completa de decisiones (la versión técnica del documento)"):
        st.markdown((A.DOCS / "bitacora_decisiones.md").read_text(encoding="utf-8"))
