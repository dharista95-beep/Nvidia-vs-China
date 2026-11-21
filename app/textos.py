"""Textos de la app en lenguaje sencillo (de consultor a cliente no técnico).

Aquí viven el glosario, la descripción de cada base de datos, las preguntas
del estudio y las recomendaciones. Si hay que cambiar una redacción, se cambia
aquí y no en el código de las páginas.
"""

# ---------------------------------------------------------------------------
# Las 4 preguntas, con un título corto que se entiende solo
# ---------------------------------------------------------------------------
PREGUNTAS = {
    "P1": {"corto": "¿Cuánto vende Nvidia en China?",
           "pregunta": "¿Cuánto pesaba China en las ventas de Nvidia antes y después de cada ronda de restricciones?",
           "palabras": "peso de China · ventas por país · antes y después de cada regla"},
    "P2": {"corto": "¿Cómo reacciona la acción?",
           "pregunta": "Cuando sale una noticia de restricciones (o de apertura), ¿la acción de Nvidia sube o baja más que el resto del mercado?",
           "palabras": "precio de la acción · noticias regulatorias · comparación con el mercado"},
    "P3": {"corto": "¿Qué compensó lo perdido en China?",
           "pregunta": "¿Las ventas en EE.UU. y de chips para centros de datos taparon lo que Nvidia dejó de vender en China?",
           "palabras": "de dónde viene el crecimiento · EE.UU. · centros de datos"},
    "P4": {"corto": "¿Crecieron los competidores chinos?",
           "pregunta": "¿Los competidores chinos (Cambricon, Hygon, SMIC) crecieron justo cuando Nvidia perdía acceso a China?",
           "palabras": "competidores chinos · crecimiento · comparación con ASML"},
}

PREGUNTA_CENTRAL = ("¿Cómo debe Nvidia, o alguien que invierte en Nvidia, manejar su dependencia del mercado chino "
                    "ahora que EE.UU. limita qué chips se le pueden vender a China?")

# ---------------------------------------------------------------------------
# Glosario
# ---------------------------------------------------------------------------
GLOSARIO = {
    # Chips y empresa
    "GPU": "Procesador gráfico. Nació para videojuegos, pero hoy es el chip más usado para entrenar y correr inteligencia artificial.",
    "Data Center (centros de datos)": "El negocio de Nvidia que vende chips para los grandes centros de cómputo de empresas como Microsoft, Google o Alibaba. Es donde está la IA y es justo lo que EE.UU. restringe. Hoy es ~90% de las ventas de Nvidia.",
    "Gaming": "El negocio de Nvidia de tarjetas gráficas para videojuegos. Antes era el principal; hoy es pequeño.",
    "A100 / H100": "Chips de IA de gama alta de Nvidia. Desde 2022 no se pueden vender a China sin permiso del gobierno de EE.UU.",
    "A800 / H800": "Versiones 'recortadas' del A100 y H100, hechas para cumplir la regla de 2022 y poder seguir vendiendo en China. Se prohibieron en octubre de 2023.",
    "H20": "Chip todavía más recortado que Nvidia diseñó para China después de 2023. En abril de 2025 EE.UU. también le exigió permiso; Nvidia tuvo que reconocer una pérdida de 4,500 millones de dólares por chips que ya no pudo vender.",
    "H200": "Chip de IA más potente que el H20. En diciembre de 2025 EE.UU. autorizó venderlo a China pagando 25% al gobierno, pero China frenó su entrada en aduanas; desde agosto de 2026 permite entregas limitadas.",
    "CUDA": "El software de Nvidia para programar sus chips. Hace que cambiarse a otro proveedor sea caro y lento, y por eso los clientes son 'leales'.",
    "TSMC": "Empresa de Taiwán que fabrica los chips que Nvidia diseña. Nvidia no tiene fábricas propias.",
    # Reglas y gobiernos
    "Controles de exportación": "Reglas del gobierno de EE.UU. que prohíben o exigen permiso para vender ciertos productos (aquí, chips avanzados) a ciertos países.",
    "Licencia (de exportación)": "Permiso caso por caso del gobierno de EE.UU. para vender un chip restringido a un cliente específico.",
    "BIS": "Oficina de Industria y Seguridad del Departamento de Comercio de EE.UU. Es quien escribe y actualiza las reglas de exportación de chips.",
    "AI Diffusion (regla de difusión de IA)": "Regla de EE.UU. anunciada en enero de 2025 que pedía licencias para vender chips de IA en casi todo el mundo. Se canceló en mayo de 2025.",
    "SAMR": "Regulador de competencia de China (como una comisión antimonopolio). Abrió una investigación a Nvidia en diciembre de 2024.",
    "CAC": "Agencia del ciberespacio de China. En septiembre de 2025 pidió a las empresas chinas dejar de comprar chips de Nvidia.",
    "IA soberana": "Inversión de gobiernos (Europa, Medio Oriente, Japón, India) en su propia infraestructura de inteligencia artificial. Es un mercado alternativo para Nvidia.",
    # Competidores y comparables
    "Cambricon": "Empresa china que diseña chips de IA. Es el competidor local más parecido a Nvidia que cotiza en bolsa.",
    "Hygon": "Empresa china que hace procesadores y chips para centros de datos.",
    "SMIC": "La mayor fábrica de chips de China (el 'TSMC chino').",
    "Huawei Ascend": "Línea de chips de IA de Huawei. Es el rival chino más fuerte, pero Huawei no cotiza en bolsa y no publica cuánto vende de estos chips, así que no entra en los números.",
    "ASML": "Empresa de Países Bajos que fabrica las máquinas para hacer chips. También tiene restricciones para vender a China; la usamos como caso de comparación.",
    "EUV / DUV": "Tipos de máquinas de ASML para 'imprimir' chips. EUV es la más avanzada (prohibida a China desde 2019); DUV es la generación anterior (parcialmente restringida desde 2023).",
    # Finanzas
    "Acción / precio ajustado": "El precio de la acción corregido por 'splits' (cuando una acción se divide en varias) y dividendos, para que se pueda comparar en el tiempo sin saltos falsos.",
    "Split": "Cuando una empresa divide cada acción en varias más baratas. Nvidia lo hizo 4 a 1 en 2021 y 10 a 1 en 2024. No cambia el valor de la empresa.",
    "S&P 500": "Índice de las 500 empresas más grandes de EE.UU. Lo usamos como 'el mercado en general'.",
    "SOX": "Índice de las principales empresas de semiconductores (chips). Lo usamos como 'el sector'.",
    "Rendimiento": "Cuánto subió o bajó el precio en un periodo, en porcentaje.",
    "Movimiento extra (rendimiento anormal, CAR)": "Cuánto se movió la acción de Nvidia por encima o por debajo de lo que 'normalmente' se habría movido ese día dado lo que hizo el mercado. En inglés se le llama CAR (cumulative abnormal return). Si es −5%, la acción perdió 5% más de lo esperado.",
    "Estudio de eventos": "Técnica para medir cuánto movió una noticia el precio de una acción: se compara lo que pasó en los días de la noticia con lo que se esperaba según el comportamiento normal de la acción frente al mercado.",
    "Beta": "Qué tanto se mueve una acción cuando se mueve el mercado. Beta 2 significa que, en promedio, si el mercado sube 1%, la acción sube 2%.",
    "Significativo (estadísticamente)": "Que el movimiento fue lo bastante grande como para que sea poco probable que haya sido casualidad. Lo marcamos con un asterisco (*).",
    "Índice base 100": "Forma de comparar cosas de distinto tamaño o moneda: el primer año vale 100, y si después vale 250 quiere decir que creció 2.5 veces.",
    "Cargo por inventario": "Pérdida contable que reconoce una empresa cuando tiene productos ya fabricados que no va a poder vender.",
    "Dilución": "Cuando el porcentaje de algo baja no porque se venda menos, sino porque lo demás creció mucho más rápido.",
    "MUSD": "Millones de dólares estadounidenses.",
    "CNY (yuanes)": "Moneda de China.",
    # Datos
    "SEC": "Comisión de Valores de EE.UU. Las empresas que cotizan en bolsa le entregan sus reportes oficiales, que son públicos.",
    "10-K / 10-Q": "Reportes oficiales que las empresas entregan a la SEC: el 10-K es el anual y el 10-Q el trimestral. Están auditados.",
    "XBRL": "Versión 'para computadora' de los reportes de la SEC: cada cifra viene etiquetada (por ejemplo 'ventas en China, tercer trimestre'), lo que evita copiar tablas a mano.",
    "Año fiscal (FY)": "El año contable de la empresa. El de Nvidia termina a finales de enero, así que el 'FY2026' va de febrero de 2025 a enero de 2026.",
    "Base facturación / base sede del cliente": "Dos formas en que Nvidia ha contado sus ventas por país. Hasta 2025: según dónde se facturaba. Desde octubre de 2025: según dónde está la oficina central del cliente. Dan números distintos, por eso nunca las mezclamos.",
    "Régimen (regulatorio)": "Periodo en el que estuvo vigente un mismo conjunto de reglas. Lo usamos para comparar 'antes' y 'después' de cada ronda de restricciones.",
    "ROCCC": "Lista para evaluar si una fuente de datos es buena: Confiable, Original, Completa, Actual y Citada.",
    "Asociación vs. causalidad": "Que dos cosas pasen al mismo tiempo (asociación) no prueba que una cause la otra (causalidad). En este estudio sólo afirmamos asociaciones.",
}

# ---------------------------------------------------------------------------
# Las bases de datos, explicadas
# ---------------------------------------------------------------------------
BASES = {
    "nvda": {
        "nombre": "Ventas de Nvidia por país y por negocio",
        "icono": "💵",
        "que_es": "Cuánto vendió Nvidia cada trimestre, separado por país (EE.UU., Taiwán, China y el resto) y por negocio (centros de datos y videojuegos). Es la base principal del estudio.",
        "fuente": "Reportes oficiales de Nvidia a la SEC (10-K y 10-Q), versión XBRL",
        "periodo": "Ago-2019 a jul-2026 (32 trimestres)",
        "preguntas": "P1 y P3",
        "confianza": "Alta: son cifras auditadas y obligatorias",
    },
    "px_us": {
        "nombre": "Precios diarios de acciones en EE.UU.",
        "icono": "📈",
        "que_es": "El precio de cierre de cada día de la acción de Nvidia, de dos empresas comparables (AMD y ASML) y de dos índices: el mercado en general (S&P 500) y el sector de chips (SOX).",
        "fuente": "Yahoo Finance",
        "periodo": "2-ene-2019 a 19-nov-2026 (casi 2,000 días)",
        "preguntas": "P2 y P4",
        "confianza": "Alta para precios de cierre",
    },
    "px_cn": {
        "nombre": "Precios diarios de competidores chinos",
        "icono": "🇨🇳",
        "que_es": "El precio diario de la acción de Cambricon, Hygon y SMIC en la bolsa de Shanghái, en yuanes.",
        "fuente": "Yahoo Finance",
        "periodo": "Jul-2020 a nov-2026",
        "preguntas": "P4",
        "confianza": "Alta para precios de cierre",
    },
    "eventos": {
        "nombre": "Calendario de noticias regulatorias",
        "icono": "📅",
        "que_es": "Las 12 noticias más importantes de restricciones o aperturas (de EE.UU. y de China) entre 2022 y 2026: qué pasó, cuándo y quién lo anunció.",
        "fuente": "Reportes de Nvidia, gobierno de EE.UU. (BIS) y prensa (Reuters, Bloomberg, FT)",
        "periodo": "Ago-2022 a ago-2026",
        "preguntas": "P2",
        "confianza": "Media-alta: fechas cruzadas con los reportes de Nvidia cuando fue posible",
    },
    "rivales": {
        "nombre": "Ventas anuales de competidores chinos",
        "icono": "🏭",
        "que_es": "Cuánto vendieron al año Cambricon, Hygon y SMIC, y cuánto crecieron.",
        "fuente": "Estados financieros vía Yahoo Finance, cotejados con sus reportes anuales",
        "periodo": "2022 a 2025",
        "preguntas": "P4",
        "confianza": "Media: fuente secundaria, sólo 4 años",
    },
    "asml": {
        "nombre": "ASML: cuánto vende en China",
        "icono": "🔬",
        "que_es": "Ventas totales de ASML y cuánto de eso fue a China, cada año. Sirve para comparar con otra empresa que también tiene restricciones.",
        "fuente": "Reportes anuales de ASML a la SEC (20-F)",
        "periodo": "2017 a 2025",
        "preguntas": "Recuadro de comparación",
        "confianza": "Alta: cifras auditadas",
    },
    "sia": {
        "nombre": "Ventas mundiales de chips",
        "icono": "🌎",
        "que_es": "Cuánto vendió toda la industria de chips en el mundo cada año. Da contexto de qué tan grande es Nvidia.",
        "fuente": "Asociación de la Industria de Semiconductores (SIA), comunicados anuales",
        "periodo": "2019 a 2025",
        "preguntas": "Contexto para P3",
        "confianza": "Alta: es la referencia de la industria",
    },
}

# Qué significa cada columna de las tablas limpias
COLUMNAS = {
    "nvda": {
        "anio_fiscal / trimestre / periodo": "Año y trimestre contable de Nvidia (ej. FY2026-Q2). El año de Nvidia termina en enero.",
        "fin": "Último día del trimestre.",
        "base": "Forma de contar ventas por país: 'facturacion' (método anterior) o 'sede_cliente' (método nuevo).",
        "total": "Ventas totales del trimestre, en millones de dólares.",
        "eeuu / taiwan / china / otros": "Ventas a cada país, en millones de dólares. China incluye Hong Kong. 'Otros' es el resto del mundo.",
        "data_center / gaming": "Ventas de chips para centros de datos y para videojuegos.",
        "pct_china / pct_eeuu / pct_dc": "Qué porcentaje del total representa China, EE.UU. y centros de datos.",
    },
    "px_us": {
        "fecha": "Día de cotización.",
        "NVDA, AMD, ASML": "Precio ajustado de cada acción, en dólares.",
        "SP500, SOX": "Valor de los índices del mercado y del sector de chips.",
        "r_*": "Cuánto subió o bajó cada serie ese día (rendimiento diario).",
    },
    "px_cn": {
        "fecha": "Día de cotización en Shanghái.",
        "688256.SS / 688041.SS / 688981.SS": "Precio de Cambricon, Hygon y SMIC, en yuanes.",
    },
    "eventos": {
        "id": "Clave del evento (E1 a E12).",
        "fecha_anuncio": "Día en que se hizo pública la noticia.",
        "fecha_reaccion": "Primer día en que la bolsa pudo reaccionar (si la noticia salió con la bolsa cerrada, es el día siguiente).",
        "origen": "Qué gobierno tomó la medida: EE.UU. o China.",
        "descripcion / fuente": "Qué pasó y dónde se publicó.",
    },
    "rivales": {
        "empresa / ticker": "Nombre y clave en bolsa.",
        "anio": "Año calendario.",
        "ingresos_millones / moneda": "Ventas del año y su moneda (CNY o USD).",
        "crec_anual_pct": "Cuánto crecieron las ventas contra el año anterior.",
    },
    "asml": {
        "anio": "Año calendario.",
        "china_meur / total_meur": "Ventas a China y ventas totales, en millones de euros.",
        "pct_china": "Porcentaje de las ventas que fue a China.",
    },
    "sia": {
        "anio": "Año calendario.",
        "ventas_globales_musd": "Ventas mundiales de chips, en millones de dólares.",
        "crec_pct": "Crecimiento contra el año anterior.",
    },
}

# ---------------------------------------------------------------------------
# Ask
# ---------------------------------------------------------------------------
PROBLEMA = """
Nvidia es la empresa que hace los chips más usados para inteligencia artificial. Desde 2022, el gobierno de
EE.UU. le prohíbe vender sus chips más potentes a China, y desde 2025 el propio gobierno chino también le
ha puesto trabas a sus empresas para comprarlos.

China llegó a ser **una de cada cuatro dólares** que vendía Nvidia (26% en 2022). Hoy es **menos de uno de
cada diez** (entre 4.5% y 8% en los últimos trimestres). Cada vez que Nvidia diseñó un chip "recortado"
para cumplir la regla, la regla cambió, y le quedaron chips sin vender: perdió **4,500 millones de dólares**
con el H20 y **400 millones** con el H200.

**El problema:** Nvidia y quienes invierten en ella dependen en parte de un mercado que se puede abrir o
cerrar de un día para otro por decisión de dos gobiernos, y no tienen una forma clara de medir esa
dependencia ni de decidir cuánto riesgo aceptar.
"""

PORQUES = [
    ("¿Por qué bajó tanto el peso de China en las ventas de Nvidia?",
     "Porque EE.UU. exigió permisos para venderle sus chips avanzados: A100/H100 en 2022, A800/H800 en 2023 y H20 en 2025."),
    ("¿Por qué esas reglas le pegaron tanto?",
     "Porque casi todo lo que vende Nvidia (90%) son chips para centros de datos, que es justo lo restringido, y China era uno de sus mayores compradores."),
    ("¿Por qué los chips 'recortados' para China no resolvieron el problema?",
     "Porque cada vez que Nvidia sacaba un chip adaptado, EE.UU. ajustaba la regla. Y desde 2025 China también pidió a sus empresas no comprarlos y frenó el H200 en la aduana."),
    ("¿Por qué China frena la compra si sus empresas necesitan los chips?",
     "Porque quiere depender menos de un proveedor que está sujeto a decisiones de EE.UU. Al mismo tiempo crecieron sus competidores locales (Cambricon pasó de 709 a 6,497 millones de yuanes de 2023 a 2025). Ojo: esto es algo que pasó al mismo tiempo, no está probado que una cosa causara la otra."),
    ("¿Por qué esto es un problema de gestión y no sólo de ventas?",
     "Porque ni Nvidia ni el inversionista controlan las reglas. Lo que sí pueden controlar es cuánto dependen de ese mercado y qué tan preparados están para cada escenario."),
]
CAUSA_RAIZ = ("Nvidia depende en parte de un mercado cuyo acceso deciden dos gobiernos, y no tiene una forma explícita "
              "de medir, limitar y protegerse de ese riesgo.")

BRECHAS = [
    ("¿Sabemos cuánto dependemos de China?", "Nvidia cambió en 2025 la forma de contar ventas por país; los números viejos y nuevos no se pueden comparar.",
     "Una medida estable de 'cuánto vendemos a China' que se pueda seguir en el tiempo.", "% de China en ventas cada trimestre"),
    ("¿Cuánta dependencia es aceptable?", "China bajó de 26% a menos de 10%, pero por las reglas, no por decisión de Nvidia.",
     "Un tope de exposición elegido a propósito.", "% de China vs. un tope propuesto"),
    ("¿Cuánto nos cuesta cada noticia?", "La acción reacciona a los anuncios, pero nadie lo mide de forma sistemática.",
     "Saber de antemano cuánto suele mover la acción una noticia así.", "Movimiento extra de la acción en días de anuncio"),
    ("¿Cuánto perdemos por chips que no se pueden vender?", "Pérdidas de 4,500 millones (H20) y 400 millones (H200).",
     "Fabricar para China sólo con permisos ya aprobados.", "Pérdidas por inventario ligadas a China"),
    ("¿Nos están reemplazando en China?", "Los competidores chinos crecen, pero no se les da seguimiento.",
     "Vigilarlos para saber si la pérdida de China es permanente.", "Crecimiento anual de Cambricon, Hygon y SMIC"),
]

# ---------------------------------------------------------------------------
# Act
# ---------------------------------------------------------------------------
RESPUESTA = ("Recomendamos tratar a China como un <b>extra posible</b>, no como parte segura del negocio: hacer los planes "
             "suponiendo que China no compra chips de centros de datos, fabricar para China sólo cuando ambos gobiernos "
             "ya dieron permiso, y medir y proteger la exposición de forma explícita. Al mismo tiempo, hay que cuidar el "
             "riesgo nuevo que dejó la salida de China: ahora Nvidia depende muchísimo de EE.UU. y de pocos clientes.")

RECOMENDACIONES_NVIDIA = [
    ("Fabricar para China sólo con doble permiso",
     "Producir chips para China sólo cuando EE.UU. dio la licencia **y** China dejó claro que permitirá la entrada.",
     "Ya se perdieron 4,900 millones de dólares en chips que no se pudieron vender (H20 y H200).",
     "Pérdidas por inventario ligadas a China", "0 por trimestre"),
    ("Planear como si China no comprara",
     "Hacer el presupuesto con China en cero para centros de datos; cualquier venta allá es un extra.",
     "China ya es sólo 5-8% de las ventas y, cuando hubo buenas noticias, la acción casi no subió.",
     "Diferencia entre lo pronosticado y lo real por China", "Menos de 1% de las ventas"),
    ("Buscar otros mercados",
     "Crecer en Europa, Medio Oriente, Japón, India ('IA soberana') y en clientes empresariales.",
     "EE.UU. ya es más de 60% de las ventas y 4 clientes concentran ~60% en algún trimestre.",
     "% de ventas fuera de EE.UU. y China", "Más de 30%"),
    ("Tener un plan para cada escenario",
     "Definir de antemano qué hacer si China se cierra, se queda igual o se abre.",
     "Hubo 12 noticias regulatorias en 4 años, de los dos gobiernos.",
     "Días entre una nueva regla y la respuesta de Nvidia", "5 días hábiles o menos"),
    ("Reportar China siempre igual",
     "Publicar las ventas por país con un solo método y mantenerlo.",
     "Con el cambio de 2025, China pesa 19% o 13% el mismo año según cómo se cuente.",
     "Trimestres comparables publicados", "8 o más"),
]

RECOMENDACIONES_INVERSIONISTA = [
    ("Valorar a Nvidia sin China",
     "Calcular cuánto vale la empresa sin ventas en China y ver cualquier apertura como un extra.",
     "Las buenas noticias movieron la acción sólo +0.5% en promedio, y varias se revirtieron.",
     "—", "—"),
    ("Protegerse en fechas de riesgo",
     "En fechas conocidas de posibles anuncios (actualizaciones de reglas, cumbres EE.UU.-China), reducir la posición o comprar protección.",
     "Las malas noticias le quitaron a la acción 3.5% extra en promedio en tres días (hasta 8.4%).",
     "Pérdida de la cartera en días de anuncio", "Menor que la de NVDA sin protección"),
    ("Vigilar la concentración, no sólo China",
     "Revisar cada trimestre cuánto depende Nvidia de EE.UU. y de sus clientes principales.",
     "EE.UU. pesa más de 60%; algunos clientes pesan 11-22% cada uno.",
     "% EE.UU. y % del mayor cliente", "Revisión trimestral"),
    ("Usar a los competidores chinos como termómetro",
     "Si Cambricon y Hygon siguen creciendo más de 50% al año, asumir que Nvidia no regresa a China.",
     "En 2025 Cambricon creció 453% y Hygon 57%.",
     "Crecimiento anual de competidores", "Revisión anual"),
    ("Desconfiar de subidas repentinas de China",
     "Si China de pronto pesa mucho más en una empresa de chips, puede ser compra de pánico antes de una restricción.",
     "En ASML, China saltó a 36% en 2024 por compras anticipadas y luego bajó.",
     "% de China en empresas del sector", "Alerta si sube más de 10 puntos en un año"),
]

LECCIONES = [
    ("Adaptar el producto a la regla compra tiempo, no acceso permanente.",
     "El A800/H800 y el H20 se prohibieron entre 12 y 15 meses después de salir."),
    ("Para vender se necesitan dos llaves: la del país que vende y la del que compra.",
     "Con permiso de EE.UU. para el H20, Nvidia sólo vendió ~60 millones porque China frenó las compras."),
    ("Fabricar antes de tener el permiso convierte el riesgo político en pérdida de dinero.",
     "Pérdidas de 4,500 millones (H20) y 400 millones (H200)."),
    ("Si lo demás crece mucho, puede esconder que un mercado se está cayendo.",
     "Hasta 2025 China seguía creciendo en dólares aunque su porcentaje bajaba; la caída real vino después."),
    ("La bolsa castiga más las malas noticias de lo que premia las buenas.",
     "−3.5% en promedio con restricciones contra +0.5% con aperturas."),
    ("Cuando sales de un mercado, alguien más ocupa tu lugar.",
     "Cambricon multiplicó casi por 9 sus ventas entre 2022 y 2025 (pasó al mismo tiempo; no está probado que sea por eso)."),
]

ESCENARIOS = [
    ("A. Se cierra todo", "Nueva regla de EE.UU. sobre el H200, o China prohíbe formalmente comprar Nvidia",
     (0, 3), "Planear sin China y vender el inventario que quede para ese mercado"),
    ("B. Apertura limitada", "Permisos caso por caso y China aprueba compras puntuales",
     (3, 10), "Fabricar sólo contra pedidos ya aprobados por ambos gobiernos"),
    ("C. Apertura amplia", "Acuerdo comercial EE.UU.-China que incluya chips de IA",
     (10, 100), "Subir la oferta poco a poco, sin comprometer inventario a largo plazo"),
]
