#!/usr/bin/env python3
"""Paso 5: hoja de respuestas para los controles de las píldoras (los cuadernillos son reutilizables).

    python 05_hoja_respuestas.py            # genera hoja_respuestas.pdf
    python 05_hoja_respuestas.py --no-pdf   # solo hoja_respuestas.md

Un folio A4 a doble cara: un nombre de alumno por cara y 4 bloques por cara (8 píldoras por folio).
Cada bloque lleva píldora, versión, fecha, las 10 preguntas con casillas A-D y una caja para el profesor.
No contiene nada secreto: se versiona junto a los scripts.
"""

import argparse
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEMES = HERE.parent.parent / "themes"
PREGUNTAS = 10

CSS = """<style>
section { place-content: flex-start !important; padding: 9mm 11mm; }
.cab { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #333; padding-bottom: 4px; margin-bottom: 6px; }
.cab h1 { font-size: 16px; margin: 0; }
.cab .cara { font-size: 12px; font-weight: 700; }
.alumno { display: flex; gap: 18px; font-size: 12px; margin-bottom: 4px; }
.alumno span { border-bottom: 1px solid #555; padding-bottom: 2px; }
.alumno .nombre { flex: 1; }
.alumno .grupo { width: 90px; }
.ayuda { font-size: 9.5px; color: #444; margin-bottom: 8px; }
.rejilla { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 12px; }
.bloque { border: 1.5px solid #333; border-radius: 5px; padding: 8px 10px 10px; }
.bloque .num { font-size: 9px; color: #666; float: right; }
.campos { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 10px; }
.campos .lbl { font-weight: 700; }
.casillas { display: inline-flex; gap: 2px; }
.casillas i { display: inline-block; width: 20px; height: 24px; border: 1.3px solid #333; }
.fecha { flex: 1; border-bottom: 1px solid #555; height: 14px; font-size: 9px; color: #777; }
.respuestas { display: grid; grid-template-columns: 1fr 1fr; column-gap: 12px; }
.fila { display: flex; align-items: center; gap: 6px; height: 54px; font-size: 13px; }
.fila b { width: 20px; text-align: right; }
.fila span { display: inline-flex; align-items: center; justify-content: center; width: 27px; height: 27px; border: 1.3px solid #333; border-radius: 4px; font-size: 10px; color: #666; }
.prof { margin-top: 8px; border-top: 1px dashed #888; padding-top: 6px; font-size: 11px; display: flex; justify-content: space-between; color: #444; }
.prof .caja { border: 1px solid #888; padding: 1px 6px; }
</style>"""


def bloque(numero: int) -> str:
    filas = "".join(
        f'<div class="fila"><b>{q}</b>' + "".join(f"<span>{l}</span>" for l in "ABCD") + "</div>"
        for q in range(1, PREGUNTAS + 1)
    )
    return f"""<div class="bloque">
<span class="num">Bloque {numero}</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas">{filas}</div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / {PREGUNTAS}</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>"""


def cara(n_cara: int) -> str:
    primero = (n_cara - 1) * 4 + 1
    bloques = "\n".join(bloque(primero + i) for i in range(4))
    return f"""<div class="cab"><h1>Digitalización — Hoja de respuestas de las píldoras</h1><span class="cara">Cara {n_cara}/2</span></div>
<div class="alumno"><span class="nombre">Nombre y apellidos:</span><span class="grupo">Grupo:</span></div>
<div class="ayuda">Marca con una <strong>X</strong> la casilla elegida. Para corregir, rellena entera la casilla equivocada y marca otra. Antes de empezar, escribe el número de <strong>píldora</strong> y la <strong>versión</strong> que figuran en tu cuadernillo (no escribas en el cuadernillo). Un bloque por control.</div>
<div class="rejilla">
{bloques}
</div>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    cabecera = "---\nmarp: true\ntheme: a4-print\npaginate: false\nbackgroundColor: white\n---\n\n"
    md = cabecera + CSS + "\n\n" + "\n---\n\n".join(cara(c) for c in (1, 2))
    origen = HERE / "hoja_respuestas.md"
    origen.write_text(md)
    print(f"OK -> {origen.name}")
    if args.no_pdf:
        return
    if not shutil.which("marp"):
        raise SystemExit("marp no está instalado (npm i -g @marp-team/marp-cli); se ha dejado solo el .md")
    destino = origen.with_suffix(".pdf")
    r = subprocess.run(
        ["marp", "--pdf", str(origen), "-o", str(destino), f"--theme-set={THEMES}"], capture_output=True, text=True
    )
    print(f"OK -> {destino.name}" if r.returncode == 0 else f"Error en marp: {r.stderr.strip()[:300]}")


if __name__ == "__main__":
    main()
