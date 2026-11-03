#!/usr/bin/env python3
"""Corrige los controles de las píldoras escaneados (cuadernillos y hojas de respuestas) y publica la tabla.

    python corregir.py claves                 # data/soluciones_pildoras.md/.json con TODAS las versiones
    python corregir.py leer LOTE [--modelo sonnet]   # Claude lee las imágenes de data/corregir/LOTE/pag_*.png
    python corregir.py corregir LOTE          # aplica las claves y actualiza data/resultados.json
    python corregir.py publicar               # regenera digitalizacion/pildoras_resultados.md
    python corregir.py iniciales              # muestra las iniciales de cada alumno

APTO con 5 o más aciertos de 10. Si un alumno repite una píldora, cuenta el último intento.
Lo normal es lanzarlo todo con corregir.sh.

Variables de entorno: AUTOCORRECTOR_DIR (def. ~/workspace/autocorrector_test: de ahí salen la lista de alumnos
y ia.py), CORREGIR_DATA (carpeta de datos, para pruebas) y CORREGIR_PAGINA (ruta de la página publicada).
"""

import argparse
import datetime
import json
import os
import sys
import unicodedata
from pathlib import Path

from common import DATA, EXAMENES, ROOT

UMBRAL = 5          # aciertos para ser APTO
PREGUNTAS = 10
N_PILDORAS = 74
LETRAS = "ABCD"
ANCHO_LECTURA = 1600

AUTO = Path(os.environ.get("AUTOCORRECTOR_DIR", "~/workspace/autocorrector_test")).expanduser()
ALUMNOS_TXT = AUTO / "examenes" / "escaneos" / "alumnos_daw.txt"
D = Path(os.environ.get("CORREGIR_DATA", DATA))
LOTES = D / "corregir"
RESULTADOS = D / "resultados.json"
SOL_MD = D / "soluciones_pildoras.md"
SOL_JSON = D / "soluciones_pildoras.json"
PAGINA = Path(os.environ.get("CORREGIR_PAGINA", ROOT.parent / "pildoras_resultados.md"))
PROMPT = ROOT / "prompts" / "leer_pildoras.md"


# ------------------------------------------------------------------ datos básicos

def alumnos() -> list[str]:
    if not ALUMNOS_TXT.exists():
        sys.exit(f"No encuentro la lista de alumnos: {ALUMNOS_TXT}\n(define AUTOCORRECTOR_DIR)")
    return [n.strip() for n in ALUMNOS_TXT.read_text().splitlines() if n.strip()]


def sin_acentos(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def iniciales(nombre: str) -> str:
    """Primera letra del primer nombre y de los dos apellidos: JUAN AMORES ESPINOSA -> J.A.E."""
    t = sin_acentos(nombre).split()
    letras = [t[0], *t[-2:]] if len(t) > 3 else t
    return ".".join(p[0].upper() for p in letras) + "."


def leer_claves() -> dict:
    if not SOL_JSON.exists():
        sys.exit("Faltan las claves: ejecuta antes `python corregir.py claves`.")
    return json.loads(SOL_JSON.read_text())


# ------------------------------------------------------------------ claves

def cmd_claves(_):
    claves = {}
    for carpeta in sorted(EXAMENES.glob("[0-9][0-9]")):
        ruta = carpeta / "versiones.json"
        if ruta.exists():
            claves[str(int(carpeta.name))] = {
                f"{e['version']:02d}": "".join(LETRAS[q["correcta"]] for q in e["preguntas"])
                for e in json.loads(ruta.read_text())
            }
    if not claves:
        sys.exit("No hay exámenes generados (data/examenes/NN/versiones.json).")
    D.mkdir(parents=True, exist_ok=True)
    SOL_JSON.write_text(json.dumps(claves, indent=1, sort_keys=True))
    md = ["# Soluciones de los controles de las píldoras", "",
          "Letra correcta de cada pregunta (1-10) en cada versión. Apto con 5 o más aciertos.", ""]
    for n in sorted(claves, key=int):
        md += [f"## Píldora {n}", "", "| Versión | " + " | ".join(str(i) for i in range(1, PREGUNTAS + 1)) + " |",
               "|---|" + "---|" * PREGUNTAS]
        md += [f"| {v} | " + " | ".join(letras) + " |" for v, letras in sorted(claves[n].items())]
        md.append("")
    SOL_MD.write_text("\n".join(md))
    print(f"{len(claves)} píldoras, {sum(len(v) for v in claves.values())} versiones -> {SOL_MD}")


# ------------------------------------------------------------------ lectura con IA

def validar(lecturas: list, claves: dict, lista: list[str]) -> list[str]:
    errores = []
    for i, e in enumerate(lecturas, 1):
        quien = f"lectura {i} ({e.get('archivo')}, {e.get('nombre') or 'sin nombre'}, P{e.get('pildora')} V{e.get('version')})"
        if e.get("nombre") not in lista:
            errores.append(f"{quien}: el nombre no está en la lista de alumnos")
        if str(e.get("pildora")) not in claves:
            errores.append(f"{quien}: no hay clave de la píldora {e.get('pildora')}")
        elif str(e.get("version")).zfill(2) not in claves[str(e["pildora"])]:
            errores.append(f"{quien}: la versión {e.get('version')} no existe en esa píldora")
        r = e.get("respuestas", "")
        if len(r) != PREGUNTAS or any(c not in LETRAS + "-" for c in r):
            errores.append(f"{quien}: respuestas inválidas {r!r}")
    return errores


def cmd_leer(a):
    from PIL import Image

    sys.path.insert(0, str(AUTO))
    try:
        from ia import lanzar_claude
    except ImportError:
        sys.exit(f"No encuentro ia.py en {AUTO} (define AUTOCORRECTOR_DIR)")
    claves = leer_claves()
    carpeta = LOTES / a.lote
    paginas = sorted(carpeta.glob("pag_*.png"))
    if not paginas:
        sys.exit(f"No hay páginas pag_*.png en {carpeta}")
    lectura = carpeta / "lectura"
    lectura.mkdir(exist_ok=True)
    for f in paginas:
        img = Image.open(f).convert("L")
        img.resize((ANCHO_LECTURA, round(img.height * ANCHO_LECTURA / img.width))).save(lectura / f.name)
    salida = carpeta / "lecturas.json"
    salida.unlink(missing_ok=True)
    prompt = PROMPT.read_text().format(
        carpeta_lectura=lectura, salida=salida, alumnos="\n".join(f"  - {n}" for n in alumnos()))
    print(f"Leyendo {len(paginas)} páginas de {a.lote} con {a.modelo}…")
    lanzar_claude(prompt, cwd=ROOT, herramientas=["Read", "Write"], modelo=a.modelo, esperado=salida,
                  add_dirs=[lectura, carpeta])
    lecturas = json.loads(salida.read_text())
    print(f"{len(lecturas)} controles leídos -> {salida}")
    errores = validar(lecturas, claves, alumnos())
    for e in errores:
        print(f"  ¡Revisar! {e}")
    for e in lecturas:
        for k, v in (e.get("dudas") or {}).items():
            print(f"  duda · {e.get('nombre')} P{e.get('pildora')} V{e.get('version')} · {k}: {v}")
    if errores:
        print(f"Corrige {salida} a mano y ejecuta `corregir`.")
        sys.exit(2)


# ------------------------------------------------------------------ corrección

def cmd_corregir(a):
    claves, lista = leer_claves(), alumnos()
    ruta = LOTES / a.lote / "lecturas.json"
    if not ruta.exists():
        sys.exit(f"No hay lecturas: {ruta}")
    lecturas = json.loads(ruta.read_text())
    errores = validar(lecturas, claves, lista)
    if errores:
        sys.exit("Hay lecturas inválidas:\n  " + "\n  ".join(errores))
    resultados = json.loads(RESULTADOS.read_text()) if RESULTADOS.exists() else {}
    vistos = set()
    for e in lecturas:
        p, v = str(e["pildora"]), str(e["version"]).zfill(2)
        correctas = claves[p][v]
        falladas = [i + 1 for i in range(PREGUNTAS) if e["respuestas"][i] != correctas[i]]
        aciertos = PREGUNTAS - len(falladas)
        resultado = "APTO" if aciertos >= UMBRAL else "NO APTO"
        previo = resultados.get(e["nombre"], {}).get(p)
        nota = ""
        if (e["nombre"], p) in vistos:
            nota = " (repetido en este lote: cuenta el último)"
        elif previo and previo["lote"] > a.lote:
            print(f"  {iniciales(e['nombre'])} · P{p}: ya hay un intento posterior ({previo['lote']}); se ignora")
            continue
        vistos.add((e["nombre"], p))
        resultados.setdefault(e["nombre"], {})[p] = {
            "resultado": resultado, "aciertos": aciertos, "version": v, "lote": a.lote}
        print(f"  {iniciales(e['nombre'])} · P{p} · V{v}: {aciertos}/{PREGUNTAS} -> {resultado}"
              f" · errores: {','.join(map(str, falladas)) or 'ninguno'}{nota}")
    D.mkdir(parents=True, exist_ok=True)
    RESULTADOS.write_text(json.dumps(resultados, ensure_ascii=False, indent=1, sort_keys=True))
    print(f"{len(lecturas)} controles corregidos -> {RESULTADOS}")


# ------------------------------------------------------------------ página publicada

CSS = """<style>
.resultados-wrap { overflow-x: auto; max-width: 100%; }
table.resultados { border-collapse: collapse; font-size: 0.78rem; white-space: nowrap; }
table.resultados th, table.resultados td { border: 1px solid #d8dbe2; padding: 3px 6px; text-align: center; }
table.resultados thead th { background: #eef1f6; position: sticky; top: 0; }
table.resultados .alumno { position: sticky; left: 0; background: #fff; font-weight: 700; text-align: left; z-index: 1; }
table.resultados thead .alumno { background: #eef1f6; }
table.resultados .total { font-weight: 700; background: #f6f7fa; }
table.resultados .apto { background: #dcfce7; color: #166534; font-weight: 600; }
table.resultados .noapto { background: #fee2e2; color: #991b1b; font-weight: 600; }
table.resultados .pendiente { color: #9aa0ab; }
</style>"""


def cmd_publicar(_):
    lista = alumnos()
    ini = {n: iniciales(n) for n in lista}
    if len(set(ini.values())) != len(ini):
        sys.exit(f"Iniciales repetidas, hay que desambiguar: {ini}")
    resultados = json.loads(RESULTADOS.read_text()) if RESULTADOS.exists() else {}
    cab = "".join(f"<th>P{n}</th>" for n in range(1, N_PILDORAS + 1))
    filas = []
    for nombre in lista:
        r = resultados.get(nombre, {})
        celdas = []
        for n in range(1, N_PILDORAS + 1):
            res = r.get(str(n), {}).get("resultado")
            if res == "APTO":
                celdas.append('<td class="apto">APTO</td>')
            elif res:
                celdas.append('<td class="noapto">NO APTO</td>')
            else:
                celdas.append('<td class="pendiente">-</td>')
        total = sum(1 for x in r.values() if x["resultado"] == "APTO")
        filas.append(f'<tr><td class="alumno">{ini[nombre]}</td><td class="total">{total}</td>' + "".join(celdas) + "</tr>")
    hoy = datetime.date.today().strftime("%d/%m/%Y")
    pagina = f"""---
layout: default
title: "Digitalización — Resultados de las píldoras"
permalink: /digitalizacion/pildoras/resultados/
---

# Resultados de los controles de las píldoras

Cada alumno aparece con sus iniciales. **APTO** = 5 o más aciertos sobre 10; **NO APTO** = menos de 5;
**-** = todavía no examinado. Si se repite un control, cuenta el último intento. El **Total** es el número de
controles superados (hay que llegar a 36). Última actualización: {hoy}.

[Volver a las píldoras]({{{{ '/digitalizacion/pildoras/' | relative_url }}}})

{CSS}

<div class="resultados-wrap">
<table class="resultados">
<thead><tr><th class="alumno">Alumno</th><th>Total</th>{cab}</tr></thead>
<tbody>
{chr(10).join(filas)}
</tbody>
</table>
</div>
"""
    PAGINA.write_text(pagina)
    aptos = sum(1 for r in resultados.values() for x in r.values() if x["resultado"] == "APTO")
    print(f"{len(lista)} alumnos, {aptos} controles APTO -> {PAGINA}")


def cmd_iniciales(_):
    for n in alumnos():
        print(f"{iniciales(n):10} {n}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("claves").set_defaults(f=cmd_claves)
    p = sub.add_parser("leer")
    p.add_argument("lote")
    p.add_argument("--modelo", default="sonnet")
    p.set_defaults(f=cmd_leer)
    p = sub.add_parser("corregir")
    p.add_argument("lote")
    p.set_defaults(f=cmd_corregir)
    sub.add_parser("publicar").set_defaults(f=cmd_publicar)
    sub.add_parser("iniciales").set_defaults(f=cmd_iniciales)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
