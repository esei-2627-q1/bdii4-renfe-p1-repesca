# -*- coding: utf-8 -*-
# Diagrama EER BDII4 :: RENFE con posiciones fijas (neato -n2).
import math
L = []
w = L.append
uid = [0]
S = 72.0 * 0.62  # pulgadas -> puntos (factor de compactación)
POS = {}

def nid(p='a'):
    uid[0] += 1
    return f"{p}{uid[0]}"

def pos(n, x, y):
    POS[n] = (x, y)
    return f'pos="{x*S:.1f},{y*S:.1f}!"'

def entity(n, x, y, weak=False, label=None):
    w(f'{n} [shape=box, style="filled", fillcolor="#dfe9f7", fontname="Helvetica-Bold", fontsize=16, '
      f'peripheries={2 if weak else 1}, label="{label or n}", {pos(n,x,y)}];')

def rel(n, x, y, label=None, ident=False):
    w(f'{n} [shape=diamond, style="filled", fillcolor="#fbeccb", fontsize=13, width=1.05, height=0.5, '
      f'peripheries={2 if ident else 1}, label="{label or n}", {pos(n,x,y)}];')

def circ(n, x, y, sym):
    w(f'{n} [shape=circle, label="{sym}", fontsize=15, width=0.32, height=0.32, fixedsize=true, {pos(n,x,y)}];')

def attr_at(owner, name, x, y, key=False, multi=False, derived=False, partial=False):
    a = nid()
    if key:
        lab = f'<<U>{name}</U>>'
    elif partial:
        lab = (f'<<TABLE BORDER="0" CELLBORDER="0" CELLPADDING="0" CELLSPACING="0"><TR>'
               f'<TD BORDER="1" SIDES="B" STYLE="dashed">{name}</TD></TR></TABLE>>')
    else:
        lab = f'"{name}"'
    style = 'dashed' if derived else 'solid'
    w(f'{a} [shape=ellipse, fontsize=13, margin="0.02,0.01", height=0.3, style="{style}", peripheries={2 if multi else 1}, label={lab}, {pos(a,x,y)}];')
    w(f'{owner} -- {a} [color="#666666"];')
    return a

def attrs(owner, specs, a0, a1, r=1.55, rx=None):
    """specs: lista de (nombre, opciones dict). Ángulos en grados, 0 = derecha, 90 = arriba."""
    ox, oy = POS[owner]
    n = len(specs)
    rx = rx or r * 1.35
    out = []
    for i, (name, o) in enumerate(specs):
        ang = math.radians(a0 if n == 1 else a0 + (a1 - a0) * i / (n - 1))
        x, y = ox + rx * math.cos(ang), oy + r * math.sin(ang)
        parts = o.pop('parts', None)
        a = attr_at(owner, name, x, y, **o)
        out.append(a)
        if parts:
            m = len(parts)
            for j, p in enumerate(parts):
                ang2 = ang + math.radians(-48 + 96 * (j / (m - 1) if m > 1 else 0.5))
                px, py = x + 1.25 * math.cos(ang2), y + 0.85 * math.sin(ang2)
                b = nid()
                w(f'{b} [shape=ellipse, fontsize=12, margin="0.02,0.01", height=0.28, label="{p}", {pos(b,px,py)}];')
                w(f'{a} -- {b} [color="#888888"];')
    return out

def link(ent, r, card, total=False, via=None, role=None):
    lab = f"{role} {card}" if role else card
    pw = 3.4 if total else 1.3
    common = f'fontsize=13, fontcolor="#0b3d78", penwidth={pw}'
    if via:
        p = nid('p')
        w(f'{p} [shape=point, width=0.01, label="", {pos(p,*via)}];')
        w(f'{ent} -- {p} [label="{lab}", {common}];')
        w(f'{p} -- {r} [{common}];')
    else:
        w(f'{ent} -- {r} [label="{lab}", {common}];')

K = {'key': True}
P = {'partial': True}
M = {'multi': True}
D = {'derived': True}

w('graph EER {')
w('  graph [splines=false, outputorder=nodesfirst, pad=0.15, bgcolor=white, fontname="Helvetica-Bold", fontsize=20, labelloc=t, '
  'label="BDII4 :: RENFE  ·  Diagrama EER  ·  cardinalidad (mín,máx) por participación; trazo grueso = participación total; subrayado discontinuo = clave parcial"];')
w('  node [fontname="Helvetica", margin="0.05,0.02"];')
w('  edge [fontname="Helvetica-Bold"];')

# ---------- Agregación VIAJE (caja dibujada primero, queda al fondo) ----------
w(f'VIAJE [shape=box, style="rounded,dashed,filled", fillcolor="#f6f9fd", color="#0b3d78", penwidth=2.5, '
  f'fixedsize=true, width=8.45, height=5.1, labelloc=t, fontname="Helvetica-Bold", fontsize=20, '
  f'fontcolor="#0b3d78", label="VIAJE (agregación)", {pos("VIAJE",20,13.3)}];')
entity('TREN', 16.3, 12.4)
entity('RUTA', 23.8, 12.4)
rel('cubre', 20, 14.6)
link('TREN', 'cubre', '(0,N)')
link('RUTA', 'cubre', '(0,N)')
attrs('cubre', [('fecha_salida', {}), ('fecha_llegada', {}), ('duracion_h', dict(D))], 140, 40, r=1.7, rx=2.4)
attr_at('TREN', 'num_serie', 16.7, 14.1, key=True)
attr_at('TREN', 'modelo', 14.9, 15.1)
attr_at('TREN', 'potencia_kw', 16.6, 10.4)
attr_at('TREN', 'fecha_fabr', 18.6, 10.7)
attr_at('TREN', 'num_max_vagones', 19.3, 11.9)
attr_at('RUTA', 'cod_ruta', 22.2, 10.9, key=True)
attr_at('RUTA', 'distancia', 25.4, 10.9)

# ---------- Personal ----------
entity('EMPLEADO', 19.5, 25.6)
attr_at('EMPLEADO', 'dni', 16.6, 26.1, key=True)
attr_at('EMPLEADO', 'nss', 18.3, 27.1)
attr_at('EMPLEADO', 'nombre', 20.6, 27.2)
attr_at('EMPLEADO', 'f_nac', 22.6, 26.6)
attr_at('EMPLEADO', 'telefono (1..2)', 16.2, 24.6, multi=True)
circ('esp_emp', 19.5, 23.6, 'd')
w('EMPLEADO -- esp_emp [penwidth=1.3];')
entity('TECNICO', 8.5, 21.3)
entity('MAQUINISTA', 15.2, 21.3)
entity('REVISOR', 23.8, 21.3)
entity('SEGURIDAD', 29.4, 21.3)
for s in ['TECNICO', 'MAQUINISTA', 'REVISOR', 'SEGURIDAD']:
    w(f'esp_emp -- {s} [penwidth=1.3];')
attr_at('TECNICO', 'especialidad', 5.4, 21.3)
attr_at('MAQUINISTA', 'horas_conduccion', 13.0, 22.8)
attr_at('REVISOR', 'idiomas', 26.2, 22.6, multi=True)
attr_at('SEGURIDAD', 'nivel', 29.4, 23.0)
rel('supervisa', 8.5, 24.8)
link('TECNICO', 'supervisa', '(0,N)', role='supervisor', via=(6.2, 23.6))
link('TECNICO', 'supervisa', '(0,1)', role='supervisado', via=(10.8, 23.6))
rel('opera', 15.2, 18.6)
link('MAQUINISTA', 'opera', '(0,N)')
w('opera -- VIAJE [label="(1,1)", fontsize=13, fontcolor="#0b3d78", penwidth=3.4];')
rel('revisa', 23.8, 18.6)
link('REVISOR', 'revisa', '(0,N)')
w('revisa -- VIAJE [label="(0,N)", fontsize=13, fontcolor="#0b3d78", penwidth=1.3];')
attr_at('revisa', 'incidencias', 26.6, 19.4)

# ---------- Estación ----------
entity('ESTACION', 36.0, 21.3)
attr_at('ESTACION', 'cod_estacion', 34.3, 23.5, key=True)
attr_at('ESTACION', 'nombre', 36.3, 24.3)
attr_at('ESTACION', 'num_vias', 38.4, 23.8)
attr_at('ESTACION', 'telefono', 38.6, 22.6)
dE = attr_at('ESTACION', 'direccion', 39.4, 21.3)
for (p, x, y) in [('calle', 41.4, 22.5), ('numero', 42.0, 21.6), ('ciudad', 41.9, 20.7), ('cp', 41.0, 19.9)]:
    b = nid(); w(f'{b} [shape=ellipse, fontsize=12, margin="0.02,0.01", height=0.28, label="{p}", {pos(b,x,y)}];'); w(f'{dE} -- {b} [color="#888888"];')
# (las partes de la dirección se enlazan abajo con el nodo correcto)
rel('controla', 32.7, 21.3)
link('SEGURIDAD', 'controla', '(1,1)', total=True)
link('ESTACION', 'controla', '(1,N)', total=True)
rel('dirige', 28.2, 25.6)
link('EMPLEADO', 'dirige', '(0,1)')
link('ESTACION', 'dirige', '(1,1)', total=True)
attr_at('dirige', 'f_inicio_jefatura', 28.2, 27.1)

entity('ANDEN', 33.2, 13.4, weak=True)
rel('tiene_anden', 35.1, 18.0, label='tiene_anden', ident=True)
link('ESTACION', 'tiene_anden', '(1,N)', total=True)
link('ANDEN', 'tiene_anden', '(1,1)', total=True)
attr_at('ANDEN', 'num_anden', 31.3, 11.9, partial=True)
attr_at('ANDEN', 'longitud', 34.7, 11.9)
rel('llega', 29.0, 13.0)
link('ANDEN', 'llega', '(0,N)')
w('llega -- VIAJE [label="(1,1)", fontsize=13, fontcolor="#0b3d78", penwidth=3.4];')

entity('TAQUILLA', 38.6, 12.6, weak=True)
rel('tiene_taq', 38.6, 17.2, label='tiene_taquilla', ident=True)
link('ESTACION', 'tiene_taq', '(1,N)', total=True)
link('TAQUILLA', 'tiene_taq', '(1,1)', total=True)
attr_at('TAQUILLA', 'num_taquilla', 41.2, 14.0, partial=True)
attr_at('TAQUILLA', 'estado', 41.4, 12.6)
attr_at('TAQUILLA', 'turno', 41.2, 11.2)

rel('origen', 28.8, 18.3)
rel('destino', 30.3, 15.8)
link('RUTA', 'origen', '(1,1)', total=True)
link('RUTA', 'destino', '(1,1)', total=True)
link('ESTACION', 'origen', '(0,N)')
link('ESTACION', 'destino', '(0,N)')

# ---------- Billete ----------
entity('BILLETE', 33.4, 6.0)
attr_at('BILLETE', 'localizador', 37.0, 5.3, key=True)
attr_at('BILLETE', 'f_compra', 38.7, 6.0)
attr_at('BILLETE', 'precio', 36.2, 3.5)
attr_at('BILLETE', 'asiento', 30.7, 3.9)
rel('vende', 37.6, 8.6)
link('TAQUILLA', 'vende', '(0,N)')
link('BILLETE', 'vende', '(1,1)', total=True)
rel('corresponde', 28.4, 7.6)
link('BILLETE', 'corresponde', '(1,1)', total=True)
w('corresponde -- VIAJE [label="(0,N)", fontsize=13, fontcolor="#0b3d78", penwidth=1.3];')
circ('esp_bil', 33.4, 3.9, 'd')
w('BILLETE -- esp_bil [color="black:invis:black", penwidth=1.6];')
entity('BILLETE_CLASICO', 30.6, 1.9)
entity('BILLETE_ESPECIAL', 36.4, 1.9)
w('esp_bil -- BILLETE_CLASICO [penwidth=1.3]; esp_bil -- BILLETE_ESPECIAL [penwidth=1.3];')
attr_at('BILLETE_CLASICO', 'tarifa', 30.6, 0.4)
attr_at('BILLETE_ESPECIAL', 'porcentaje_dto', 35.2, 0.4)
attr_at('BILLETE_ESPECIAL', 'motivo_dto', 38.4, 0.4)

# ---------- Pasajero ----------
entity('PASAJERO', 22.6, 4.6)
attrs('PASAJERO', [('dni', dict(K)), ('nombre', {}), ('correo', {}), ('f_nac', {}), ('edad', dict(D))], 160, 35, r=1.35, rx=2.6)
rel('compra', 27.6, 4.6)
link('PASAJERO', 'compra', '(1,N)', total=True)
link('BILLETE', 'compra', '(1,1)', total=True)
rel('genera', 25.4, 2.4)
link('PASAJERO', 'genera', '(0,N)')
entity('RECLAMACION', 25.4, 0.6)
link('RECLAMACION', 'genera', '(1,1)', total=True)
attr_at('RECLAMACION', 'id_reclamacion', 23.0, -0.7, key=True)
attr_at('RECLAMACION', 'fecha', 28.0, 1.2)
attr_at('RECLAMACION', 'motivo', 28.2, 0.0)
rel('lleva', 19.4, 3.0, ident=True)
link('PASAJERO', 'lleva', '(0,N)')
entity('BULTO', 19.4, 0.9, weak=True)
link('BULTO', 'lleva', '(1,1)', total=True)
attr_at('BULTO', 'num_bulto', 16.6, 1.9, partial=True)
attr_at('BULTO', 'peso_kg', 16.4, 0.6)
dim = attr_at('BULTO', 'dimensiones', 17.4, -0.6)
for p, x, y in [('ancho_cm', 15.3, -1.3), ('largo_cm', 19.6, -1.3)]:
    b = nid(); w(f'{b} [shape=ellipse, fontsize=12, margin="0.02,0.01", height=0.28, label="{p}", {pos(b,x,y)}];'); w(f'{dim} -- {b} [color="#888888"];')

# ---------- Tren: generalización y subclase compartida ----------
circ('gen_tren', 12.0, 7.6, 'o')
w('TREN -- gen_tren [color="black:invis:black", penwidth=1.6];')
entity('TREN_PASAJEROS', 9.0, 5.8)
entity('TREN_MERCANCIA', 15.0, 5.8)
w('gen_tren -- TREN_PASAJEROS [penwidth=1.3]; gen_tren -- TREN_MERCANCIA [penwidth=1.3];')
circ('sh_tren', 12.0, 3.7, '∩')
w('TREN_PASAJEROS -- sh_tren [penwidth=1.3]; TREN_MERCANCIA -- sh_tren [penwidth=1.3];')
entity('TREN_MIXTO', 12.0, 1.9)
w('sh_tren -- TREN_MIXTO [penwidth=1.3];')
attr_at('TREN_PASAJEROS', 'clase', 6.3, 5.0)
attr_at('TREN_MERCANCIA', 'tipo_mercancia', 15.6, 4.2)
attr_at('TREN_MIXTO', 'carga_max_con_pasaje', 12.0, 0.4)

# ---------- Vagón ----------
entity('VAGON', 6.2, 12.4, weak=True)
rel('compone', 10.6, 12.4, ident=True)
w('TREN -- compone [taillabel="(1,N)", labeldistance=3.2, labelangle=-25, fontsize=13, fontcolor="#0b3d78", penwidth=3.4];')
link('VAGON', 'compone', '(1,1)', total=True)
attr_at('VAGON', 'num_vagon', 3.4, 11.2, partial=True)
attr_at('VAGON', 'tipo_vagon', 5.0, 10.3)
attr_at('VAGON', 'plazas', 6.9, 10.2)
attr_at('VAGON', 'toneladas', 8.7, 10.6)
attr_at('VAGON', 'anho_fab', 8.6, 11.6)
rel('acopla', 2.4, 15.2)
link('VAGON', 'acopla', '(0,1)', role='precede', via=(3.0, 12.6))
link('VAGON', 'acopla', '(0,1)', role='sigue', via=(5.6, 15.6))

# ---------- Almacén ----------
entity('ALMACEN', 3.4, 8.2)
rel('guarda', 8.4, 9.4)
link('ALMACEN', 'guarda', '(0,N)')
link('TREN', 'guarda', '(1,1)', total=True)
attr_at('ALMACEN', 'cod_alm', 0.6, 9.2, key=True)
attr_at('ALMACEN', 'telefono', 2.9, 9.7)
attr_at('ALMACEN', 'max_trenes', 5.9, 7.1)
dA = attr_at('ALMACEN', 'direccion', 1.0, 6.3)
for p, x, y in [('calle', -0.6, 7.2), ('numero', -0.8, 6.0), ('ciudad', -0.4, 4.9), ('cp', 1.0, 4.6)]:
    b = nid(); w(f'{b} [shape=ellipse, fontsize=12, margin="0.02,0.01", height=0.28, label="{p}", {pos(b,x,y)}];'); w(f'{dA} -- {b} [color="#888888"];')

# ---------- Mantenimiento ----------
rel('instala', 9.6, 17.6)
link('TECNICO', 'instala', '(0,N)')
link('TREN', 'instala', '(0,N)')
entity('PIEZA', 3.6, 18.8)
link('PIEZA', 'instala', '(0,N)')
attr_at('instala', 'fecha_instalacion', 8.4, 16.3, multi=True)
attr_at('PIEZA', 'cod_pieza', 0.6, 18.0, key=True)
attr_at('PIEZA', 'nombre', 0.6, 19.4)
attr_at('PIEZA', 'descripcion', 1.4, 17.0)
attr_at('PIEZA', 'precio', 4.0, 17.2)
rel('suministra', 1.8, 21.6)
link('PIEZA', 'suministra', '(1,1)', total=True)
entity('PROVEEDOR', 1.8, 24.6)
link('PROVEEDOR', 'suministra', '(1,N)', total=True)
attr_at('PROVEEDOR', 'cif', -0.9, 23.6, key=True)
attr_at('PROVEEDOR', 'nombre', -0.9, 25.6)
attr_at('PROVEEDOR', 'email', 4.4, 26.0)
dP = attr_at('PROVEEDOR', 'direccion', 1.8, 26.6)
for p, x, y in [('calle', -0.6, 27.4), ('numero', 1.0, 27.9), ('ciudad', 2.8, 27.9), ('cp', 4.2, 27.4)]:
    b = nid(); w(f'{b} [shape=ellipse, fontsize=12, margin="0.02,0.01", height=0.28, label="{p}", {pos(b,x,y)}];'); w(f'{dP} -- {b} [color="#888888"];')

w('}')
txt = '\n'.join(L)
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'eer.dot'), 'w', encoding='utf-8').write(txt)
print('ok')
