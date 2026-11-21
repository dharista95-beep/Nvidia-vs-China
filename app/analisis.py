"""Carga de datos y cálculos del estudio Nvidia-China.

Reutiliza las tablas limpias de data/clean y la misma lógica de los notebooks
(01_prepare_process y 02_analyze_share). No descarga nada de internet.
"""
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent.parent      # carpeta nvidia_china/
RAW = BASE / "data" / "raw"
CLEAN = BASE / "data" / "clean"
FIG = BASE / "figuras"
DOCS = BASE / "docs"

# Paleta validada (la misma de las figuras del PDF): azul = Nvidia/apertura, naranja = China/restricción
AZUL, NARANJA, VERDE, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984"

# Rondas de controles que se marcan en las gráficas (fecha en que el mercado pudo reaccionar)
RONDAS = [("2022-09-01", "Controles 2022"), ("2023-10-17", "Controles oct-2023"),
          ("2025-04-16", "Licencia H20"), ("2025-12-08", "H200 con licencia")]

# Clasificación de eventos (decisión A-05 de la bitácora)
TIPO_EVENTO = {"E1": "Restricción", "E2": "Restricción", "E3": "Restricción", "E4": "Restricción",
               "E5": "Restricción", "E6": "Restricción", "E7": "Apertura", "E8": "Apertura",
               "E9": "Restricción", "E10": "Apertura", "E11": "Restricción", "E12": "Apertura"}

NOMBRE_BASE = {"facturacion": "Base facturación (hasta jul-2025)",
               "sede_cliente": "Base sede del cliente (desde oct-2024)"}


# ---------------------------------------------------------------- carga
def cargar():
    """Devuelve un diccionario con todas las tablas limpias."""
    d = {}
    d["q"] = pd.read_csv(CLEAN / "nvda_ingresos_trimestrales.csv", parse_dates=["fin"])
    d["largo"] = pd.read_csv(CLEAN / "nvda_ingresos_trimestrales_largo.csv")
    d["an"] = pd.read_csv(CLEAN / "nvda_ingresos_anuales.csv")
    d["px"] = pd.read_csv(CLEAN / "precios_diarios_eeuu.csv", parse_dates=["fecha"]).set_index("fecha")
    d["pxcn"] = pd.read_csv(CLEAN / "precios_diarios_rivales_china.csv", parse_dates=["fecha"]).set_index("fecha")
    d["ev"] = pd.read_csv(CLEAN / "eventos_controles_exportacion.csv", parse_dates=["fecha_anuncio", "fecha_reaccion"])
    d["ev"]["tipo"] = d["ev"].id.map(TIPO_EVENTO)
    d["riv"] = pd.read_csv(CLEAN / "rivales_china_ingresos_anuales.csv")
    d["asml"] = pd.read_csv(CLEAN / "asml_ingresos_china_anual.csv")
    d["sia"] = pd.read_csv(CLEAN / "semiconductores_ventas_globales_sia.csv")
    return d


def cargar_raw():
    """Datos crudos, para comparar antes y después de la limpieza."""
    return {"xbrl": pd.read_csv(RAW / "nvda_xbrl_ingresos_raw.csv"),
            "px_us": pd.read_csv(RAW / "precios_ajustados_eeuu_raw.csv"),
            "px_cn": pd.read_csv(RAW / "precios_ajustados_china_raw.csv")}


# Mapa de dimensiones XBRL que se conservan (decisiones D-03 y D-04)
MAPA_XBRL = {
    "TOTAL": "total",
    "srt:StatementGeographicalAxis=country:US": "eeuu",
    "srt:StatementGeographicalAxis=country:TW": "taiwan",
    "srt:StatementGeographicalAxis=nvda:ChinaIncludingHongKongMember": "china",
    "srt:StatementGeographicalAxis=country:CN": "china",
    "srt:ProductOrServiceAxis=nvda:DataCenterMember": "data_center",
    "srt:ProductOrServiceAxis=nvda:GamingMember": "gaming",
}


def validaciones(d):
    """Repite sobre las tablas limpias las validaciones del notebook de Process."""
    q, an, px, ev = d["q"], d["an"], d["px"], d["ev"]
    fact = q[q.base == "facturacion"]
    largo = d["largo"]
    tot_q = largo[largo.variable == "total"].groupby("anio_fiscal").valor_musd.agg(["sum", "count"])
    comp = tot_q[tot_q["count"] == 4].join(an.set_index("anio_fiscal").total, how="inner")
    a26 = an.set_index("anio_fiscal").loc[2026]
    r = px.filter(like="r_").dropna()
    filas = [
        ("V1", "Las regiones no exceden el total (otros ≥ 0)", bool((q.otros >= -1).all())),
        ("V2", "El 4.º trimestre derivado no es negativo",
         bool((largo[largo.origen != "reportado"].valor_musd >= 0).all())),
        ("V3", "Suma de 4 trimestres = total anual reportado",
         bool(np.allclose(comp["sum"], comp.total, rtol=1e-6))),
        ("V4", "Data Center ≤ total", bool((q.data_center <= q.total).all())),
        ("V5", "Serie en base facturación completa (24 trimestres, sin repetidos)",
         bool(len(fact) == 24 and fact.periodo.is_unique)),
        ("V6", "Cotejo con el 10-K FY2026: China 19,677 y total 215,938 MUSD",
         bool(round(a26.china_sede_cliente) == 19677 and round(a26.total) == 215938)),
        ("Precios", "Sin faltantes en EE.UU. y ningún rendimiento diario mayor a ±50%",
         bool(px.drop(columns=r.columns).notna().all().all() and (r.abs() < 0.5).all().all())),
        ("Eventos", "Las 12 fechas de reacción son días con cotización",
         bool(ev.fecha_reaccion.isin(px.index).all())),
    ]
    return pd.DataFrame(filas, columns=["id", "validación", "ok"])


# ---------------------------------------------------------------- P1
def regimen(periodo):
    """Asigna cada trimestre fiscal a un régimen regulatorio (igual que el notebook)."""
    fy, t = int(periodo[2:6]), int(periodo[-1])
    k = fy * 10 + t
    if k <= 20232:
        return "R0 Sin controles"
    if k <= 20243:
        return "R1 Controles 2022"
    if k <= 20261:
        return "R2 Controles oct-2023"
    return "R3 Licencia H20 / H200"


def tabla_regimenes(q):
    q = q.assign(regimen=q.periodo.map(regimen))
    return (q.groupby(["base", "regimen"])
             .agg(trimestres=("periodo", "count"), desde=("periodo", "first"), hasta=("periodo", "last"),
                  china_prom_musd=("china", "mean"), pct_china_prom=("pct_china", "mean"),
                  pct_china_min=("pct_china", "min"), pct_china_max=("pct_china", "max"))
             .round(1).reset_index())


# ---------------------------------------------------------------- P2
def car(px, fecha, mercado="SP500", est=(-250, -11), ventana=(-1, 1)):
    """Rendimiento anormal acumulado (modelo de mercado), igual que el notebook."""
    i0 = px.index.get_indexer([fecha])[0]
    e = px.iloc[i0 + est[0]: i0 + est[1] + 1]
    w = px.iloc[i0 + ventana[0]: i0 + ventana[1] + 1]
    b, a = np.polyfit(e[f"r_{mercado}"], e["r_NVDA"], 1)
    sigma = (e["r_NVDA"] - (a + b * e[f"r_{mercado}"])).std(ddof=2)
    ar = w["r_NVDA"] - (a + b * w[f"r_{mercado}"])
    c = ar.sum()
    return {"beta": b, "CAR_pct": 100 * (np.exp(c) - 1), "t": c / (sigma * np.sqrt(len(w)))}


def estudio_eventos(px, ev, mercado, ventana):
    filas = []
    for _, r in ev.iterrows():
        res = car(px, r.fecha_reaccion, mercado, ventana=ventana)
        filas.append({"id": r.id, "fecha": r.fecha_reaccion.date(), "origen": r.origen, "tipo": r.tipo,
                      "descripcion": r.descripcion, **res})
    out = pd.DataFrame(filas)
    out["significativo_5pct"] = out.t.abs() > 1.96
    return out


def trayectoria_evento(px, fecha, mercado="SP500", dias=10, est=(-250, -11)):
    """Rendimiento anormal acumulado día por día alrededor de un evento (para la gráfica de detalle)."""
    i0 = px.index.get_indexer([fecha])[0]
    e = px.iloc[i0 + est[0]: i0 + est[1] + 1]
    b, a = np.polyfit(e[f"r_{mercado}"], e["r_NVDA"], 1)
    w = px.iloc[i0 - dias: i0 + dias + 1]
    ar = w["r_NVDA"] - (a + b * w[f"r_{mercado}"])
    return pd.DataFrame({"dia": range(-dias, dias + 1),
                         "CAR_pct": 100 * (np.exp(ar.cumsum()) - 1),
                         "NVDA_pct": 100 * (np.exp(w["r_NVDA"].cumsum()) - 1),
                         "mercado_pct": 100 * (np.exp(w[f"r_{mercado}"].cumsum()) - 1)})


# ---------------------------------------------------------------- P3
def descomposicion(an, base, y0, y1):
    """Cuánto aportó cada región al cambio de ingresos entre dos años fiscales (misma base)."""
    a = an.set_index("anio_fiscal")
    reg = {"EE.UU.": f"eeuu_{base}", "Taiwán": f"taiwan_{base}", "China": f"china_{base}"}
    cambio = {k: a.loc[y1, v] - a.loc[y0, v] for k, v in reg.items()}
    otros = lambda y: a.loc[y, "total"] - a.loc[y, list(reg.values())].sum()
    cambio["Otros"] = otros(y1) - otros(y0)
    out = pd.DataFrame({"region": list(cambio), "cambio_musd": list(cambio.values())})
    out["pct_del_cambio"] = 100 * out.cambio_musd / out.cambio_musd.sum()
    return out


def anios_disponibles(an, base):
    return an.dropna(subset=[f"china_{base}"]).anio_fiscal.astype(int).tolist()


# ---------------------------------------------------------------- P4
def indice_rivales(riv, anio_base=2022):
    r = riv.pivot(index="anio", columns="empresa", values="ingresos_millones")
    return (100 * r / r.loc[anio_base]).round(0)


def rend_normalizado(px, pxcn, desde):
    """Precio de cada serie con base 100 en la fecha elegida (cada una en su moneda)."""
    series = {"NVDA": px.NVDA, "S&P 500": px.SP500, "SOX": px.SOX,
              "Cambricon": pxcn["688256.SS"], "Hygon": pxcn["688041.SS"], "SMIC (Shanghái)": pxcn["688981.SS"]}
    out = {}
    for k, s in series.items():
        s = s.dropna()
        s = s[s.index >= pd.Timestamp(desde)]
        if len(s):
            out[k] = 100 * s / s.iloc[0]
    return pd.DataFrame(out)


# ---------------------------------------------------------------- documentos
def seccion_md(archivo, titulo):
    """Texto de una sección '## titulo...' de un documento de docs/, hasta la siguiente sección."""
    texto = (DOCS / archivo).read_text(encoding="utf-8")
    partes = texto.split("\n## ")
    for p in partes[1:]:
        if p.startswith(titulo):
            cuerpo = p.split("\n", 1)[1] if "\n" in p else ""
            return cuerpo.split("\n---")[0].split("\n# ")[0].strip()
    return ""


# ---------------------------------------------------------------- Modelo de proyección (pestaña Modelo)
MODELOS = {
    "ingenuo": "Ingenuo: igual que el último trimestre",
    "crecimiento": "Crecimiento promedio reciente",
    "tendencia": "Tendencia (regresión lineal sobre el logaritmo de las ventas)",
}


def serie_total(q):
    """Ventas totales por trimestre, sin repetir trimestres (el total no depende de la forma de contar por país)."""
    t = q.sort_values(["fin", "base"]).drop_duplicates("fin", keep="last")
    return t[["periodo", "fin", "total"]].reset_index(drop=True)


def pronostico(y, modelo, ventana, h):
    """Pronostica h trimestres hacia adelante a partir de la serie y (ventas, en MUSD).

    Se trabaja con logaritmos para que el modelo piense en % de crecimiento y no en montos.
    """
    ly = np.log(np.asarray(y, dtype=float))
    pasos = np.arange(1, h + 1)
    if modelo == "ingenuo":
        return np.exp(np.repeat(ly[-1], h))
    w = min(ventana, len(ly))
    if modelo == "crecimiento":
        g = np.diff(ly[-w:]).mean()                     # crecimiento promedio por trimestre
        return np.exp(ly[-1] + g * pasos)
    x = np.arange(len(ly))
    b, a = np.polyfit(x[-w:], ly[-w:], 1)               # tendencia: log(ventas) = a + b·t
    return np.exp(a + b * (len(ly) - 1 + pasos))


def prueba_historica(y, modelo, ventana, desde, hasta):
    """Prueba 'como si estuviéramos en el pasado': para cada trimestre i entre desde y hasta-1,
    entrena sólo con los trimestres anteriores, pronostica el trimestre i y compara con lo que realmente pasó."""
    y = np.asarray(y, dtype=float)
    filas = []
    for i in range(desde, hasta):
        p = pronostico(y[:i], modelo, ventana, 1)[0]
        filas.append({"i": i, "real": y[i], "pronostico": p, "error_pct": 100 * (p - y[i]) / y[i]})
    return pd.DataFrame(filas)


def elegir_modelo(y, n_validacion=8, n_prueba=4, ventanas=(4, 8, 12)):
    """Entrena todas las combinaciones modelo × ventana y mide MAPE, MAE y RMSE.

    Se elige con el MAPE de validación (error en %), porque las ventas crecieron de ~3 a ~96 mil MUSD por
    trimestre y un error en millones pesaría mucho más en los trimestres recientes.

    - Validación (n_validacion trimestres antes de la prueba): sirve para ELEGIR el mejor.
    - Prueba (últimos n_prueba trimestres): se usa sólo al final, para medir el error del elegido
      con datos que no influyeron en la elección.
    """
    n = len(y)
    v0, p0 = n - n_prueba - n_validacion, n - n_prueba
    filas = []
    for m in MODELOS:
        for w in ([1] if m == "ingenuo" else ventanas):
            val = prueba_historica(y, m, w, v0, p0)
            pru = prueba_historica(y, m, w, p0, n)
            fila = {"modelo": m, "ventana": w}
            for nombre, r in [("validacion", val), ("prueba", pru)]:
                e = r.pronostico - r.real                                   # error en millones de USD
                fila[f"error_{nombre}_pct"] = r.error_pct.abs().mean()       # MAPE: error promedio en %
                fila[f"mae_{nombre}"] = e.abs().mean()                       # MAE: error promedio en MUSD
                fila[f"rmse_{nombre}"] = float(np.sqrt((e ** 2).mean()))     # RMSE: castiga más los errores grandes
            filas.append(fila)
    return pd.DataFrame(filas).sort_values("error_validacion_pct").reset_index(drop=True)
