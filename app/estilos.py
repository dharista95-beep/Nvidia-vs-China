"""Piezas visuales compartidas: tarjetas, títulos de sección, tablas y cajas de explicación.

Colores fijos y tenues (azul, rosa, gris, blanco) para que se vean igual en tema claro u oscuro.
"""
import html

import pandas as pd
import streamlit as st

# Paleta de las gráficas (la misma de las figuras del documento)
AZUL, NARANJA, VERDE, GRIS, MORADO = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#8b5cf6"

CSS = """<style>
.nv-sub{font-size:.95rem;color:#6B7280;margin:-6px 0 14px 0}
.nv-seccion{font-size:1.2rem;font-weight:700;color:#1F2937;margin:22px 0 2px 0;padding-bottom:6px;border-bottom:2px solid #F3CFDC}
.nv-seccion-sub{font-size:.88rem;color:#6B7280;margin:4px 0 10px 0}
.nv-tarjeta{border-radius:14px;padding:12px 16px;border:1px solid;min-height:104px;margin-bottom:10px;box-shadow:0 1px 3px rgba(17,24,39,.05)}
.nv-et{font-size:.85rem;font-weight:600;color:#4B5563}
.nv-ico{font-size:1.15rem;margin-right:6px;vertical-align:middle}
.nv-val{font-size:1.75rem;font-weight:800;color:#111827;line-height:1.2;margin-top:4px}
.nv-val-s{font-size:1.05rem;font-weight:700;color:#111827;line-height:1.3;margin-top:6px}
.nv-det{font-size:.78rem;color:#6B7280;margin-top:2px;line-height:1.3}
.nv-azul{background:#EEF4FB;border-color:#D5E3F4}
.nv-rosa{background:#FDF0F4;border-color:#F5D5E0}
.nv-gris{background:#F5F6F8;border-color:#E2E5EA}
.nv-blanco{background:#FFFFFF;border-color:#E5E7EB}
.nv-verde{background:#EEF8F3;border-color:#CDEBDD}
.nv-explica{background:#FFFFFF;border:1px solid #E5E7EB;border-left:5px solid #8DB4E2;border-radius:12px;padding:10px 16px;color:#1F2937;margin:4px 0 18px 0;font-size:.93rem;line-height:1.5}
.nv-explica b{color:#111827}
.nv-explica .nv-clave{display:block;margin-top:6px;padding-top:6px;border-top:1px dashed #E5E7EB}
.nv-pregunta{background:#FFFFFF;border:1px solid #E5E7EB;border-left:5px solid #E58AA8;border-radius:12px;padding:12px 16px;color:#1F2937;margin-bottom:10px}
.nv-pregunta .nv-pq{font-size:1.15rem;font-weight:700;color:#111827}
.nv-pregunta small{display:block;color:#6B7280;margin-top:4px;font-size:.85rem}
.nv-caja{overflow:auto;border:1px solid #E3E8EF;border-radius:12px;background:#FFFFFF;margin-bottom:10px}
.nv-tabla{border-collapse:collapse;width:100%;font-size:.86rem;color:#1F2937}
.nv-tabla th{position:sticky;top:0;background:#EAF1FA;color:#1F2937;font-weight:700;text-align:left;padding:8px 12px;border-bottom:2px solid #F0C6D5}
.nv-tabla td{padding:7px 12px;border-bottom:1px solid #EEF0F3;color:#1F2937;vertical-align:top}
.nv-tabla tbody tr:nth-child(even){background:#FAFBFD}
.nv-tabla th.d,.nv-tabla td.d{text-align:right;white-space:nowrap}
.nv-badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap}
.nv-b-azul{background:#DDE9F8;color:#2F5F98}
.nv-b-rosa{background:#F9DDE7;color:#A8456B}
.nv-b-gris{background:#ECEEF1;color:#4B5563}
.nv-b-verde{background:#D8F1E5;color:#1D6B4A}
.nv-nulo{display:inline-block;padding:1px 8px;border-radius:6px;background:#F9DDE7;color:#A8456B;font-size:.75rem;font-style:italic}
.nv-paso{display:flex;gap:12px;margin-bottom:10px}
.nv-num{flex:0 0 30px;height:30px;border-radius:50%;background:#DDE9F8;color:#2F5F98;font-weight:700;display:flex;align-items:center;justify-content:center}
.nv-paso-txt{flex:1;color:#1F2937;font-size:.93rem}
.nv-paso-txt b{display:block;color:#111827}
</style>"""


def iniciar():
    st.markdown(CSS, unsafe_allow_html=True)


def titulo(texto, subtitulo=""):
    st.title(texto)
    if subtitulo:
        st.markdown(f'<div class="nv-sub">{html.escape(subtitulo)}</div>', unsafe_allow_html=True)


def seccion(texto, subtitulo=""):
    st.markdown(f'<div class="nv-seccion">{html.escape(texto)}</div>'
                + (f'<div class="nv-seccion-sub">{subtitulo}</div>' if subtitulo else ""), unsafe_allow_html=True)


def tarjeta(etiqueta, valor, detalle="", color="azul", icono=""):
    return (f'<div class="nv-tarjeta nv-{color}"><div class="nv-et"><span class="nv-ico">{icono}</span>'
            f'{html.escape(etiqueta)}</div><div class="{"nv-val-s" if len(str(valor)) > 16 else "nv-val"}">{html.escape(str(valor))}</div>'
            f'<div class="nv-det">{html.escape(detalle)}</div></div>')


def tarjetas(lista):
    """lista de tuplas (etiqueta, valor, detalle, color, icono) en una fila."""
    cols = st.columns(len(lista))
    for c, t in zip(cols, lista):
        c.markdown(tarjeta(*t), unsafe_allow_html=True)


def explicacion(como_leer, que_nos_dice):
    """Caja de texto bajo cada gráfica: cómo se lee y qué conclusión sacar."""
    st.markdown(f'<div class="nv-explica"><b>¿Cómo se lee?</b> {como_leer}'
                f'<span class="nv-clave"><b>¿Qué nos dice?</b> {que_nos_dice}</span></div>', unsafe_allow_html=True)


def pregunta(clave, p):
    st.markdown(f'<div class="nv-pregunta"><div class="nv-pq">{clave}. {html.escape(p["pregunta"])}</div>'
                f'<small>Palabras clave: {html.escape(p["palabras"])}</small></div>', unsafe_allow_html=True)


def badge(texto, color):
    return f'<span class="nv-badge nv-b-{color}">{html.escape(str(texto))}</span>'


def _celda(v):
    if v is None or (not isinstance(v, str) and pd.isna(v)):
        return '<span class="nv-nulo">vacío</span>'
    if isinstance(v, float):
        return f"{v:,.0f}" if abs(v) >= 100 or v.is_integer() else f"{v:,.2f}"
    if isinstance(v, int):
        return f"{v:,}"
    return html.escape(str(v))


def tabla(datos, html_cols=(), derecha=(), alto=420):
    """Tabla con formato propio. html_cols: columnas que ya traen HTML (badges)."""
    cols = list(datos.columns)
    enc = "".join(f'<th class="{"d" if c in derecha else ""}">{html.escape(str(c))}</th>' for c in cols)
    filas = []
    for fila in datos.itertuples(index=False, name=None):
        celdas = [f'<td class="{"d" if c in derecha else ""}">{v if c in html_cols else _celda(v)}</td>'
                  for c, v in zip(cols, fila)]
        filas.append("<tr>" + "".join(celdas) + "</tr>")
    st.markdown(f'<div class="nv-caja" style="max-height:{alto}px"><table class="nv-tabla"><thead><tr>{enc}</tr></thead>'
                f'<tbody>{"".join(filas)}</tbody></table></div>', unsafe_allow_html=True)


def pasos(lista):
    """Lista numerada vertical (para los 5 porqués)."""
    for i, (t, d) in enumerate(lista, 1):
        st.markdown(f'<div class="nv-paso"><div class="nv-num">{i}</div><div class="nv-paso-txt">'
                    f'<b>{html.escape(t)}</b>{html.escape(d)}</div></div>', unsafe_allow_html=True)


def fig(f, titulo_, alto=420, leyenda=None, unificado=True):
    """Formato común de las gráficas: título con la conclusión y leyenda con título claro."""
    f.update_layout(title=dict(text=titulo_, font=dict(size=16)), height=alto, template="plotly_white",
                    hovermode="x unified" if unificado else "closest",
                    legend=dict(orientation="h", y=-0.2, title=dict(text=f"<b>{leyenda}</b>  " if leyenda else "")),
                    margin=dict(t=60, l=10, r=10, b=10), font=dict(size=13))
    return f


def mostrar(f):
    st.plotly_chart(f, width="stretch")
