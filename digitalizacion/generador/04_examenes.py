#!/usr/bin/env python3
"""Paso 4: compone las versiones de examen de cada píldora a partir de su banco.

    python 04_examenes.py --pildora 1
    python 04_examenes.py --all --versiones 10 --preguntas 10 --seed 1

Salida (data/examenes/NN/): pildora_NN_examen.md (+ .pdf si hay marp), pildora_NN_soluciones.md y versiones.json
"""

import argparse
import html
import json
import random
import re
import shutil
import subprocess
from collections import Counter

from common import BANCOS, EXAMENES, ROOT, argumentos_pildoras, seleccionar

LETRAS = "ABCD"
THEMES = ROOT.parent.parent / "themes"

CSS = """<style>
section { place-content: flex-start !important; }
.exam-header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #333; padding-bottom: 6px; margin-bottom: 4px; }
.exam-header h1 { font-size: 18px; margin: 0; }
.exam-header .version { font-size: 16px; font-weight: 700; }
.exam-subtitle { font-size: 11px; color: #444; margin-bottom: 8px; }
.exam-fields { display: flex; gap: 24px; font-size: 12px; margin-bottom: 8px; }
.exam-fields span { border-bottom: 1px solid #888; padding-bottom: 2px; flex: 1; }
.exam-instructions { font-size: 11px; color: #444; margin-bottom: 10px; }
.exam-questions { columns: 2; column-gap: 10mm; font-size: 11.5px; line-height: 1.3; }
.exam-q { break-inside: avoid; margin-bottom: 11px; }
.exam-q .stem { font-weight: 600; margin-bottom: 3px; }
.exam-q .opt { margin-left: 4px; }
.exam-q code { background: #eef0f4; border-radius: 3px; padding: 0 3px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
</style>"""


def inline(texto: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(texto, quote=False))


def elegir_preguntas(banco: list[dict], k: int, versiones: int, rng: random.Random) -> list[list[dict]]:
    """Reparte el uso de las preguntas y minimiza el solapamiento entre versiones."""
    uso, hechas, resultado = Counter(), [], []
    for _ in range(versiones):
        mejor = None
        for _ in range(300):
            cand = sorted(banco, key=lambda q: (uso[q["id"]], rng.random()))[:k]
            ids = {q["id"] for q in cand}
            solape = max((len(ids & h) for h in hechas), default=0)
            puntuacion = (solape, sum(uso[i] for i in ids), rng.random())
            if mejor is None or puntuacion < mejor[0]:
                mejor = (puntuacion, cand)
        resultado.append(mejor[1])
        for q in mejor[1]:
            uso[q["id"]] += 1
        hechas.append({q["id"] for q in mejor[1]})
    return resultado


def montar_version(preguntas: list[dict], rng: random.Random) -> list[dict]:
    """Baraja orden de preguntas y de opciones; evita repartos de letras muy desequilibrados."""
    tope = -(-len(preguntas) // 4)
    for _ in range(500):
        orden = preguntas[:]
        rng.shuffle(orden)
        montadas = []
        for q in orden:
            perm = list(range(4))
            rng.shuffle(perm)
            montadas.append(
                {
                    "id": q["id"],
                    "pregunta": q["pregunta"],
                    "opciones": [q["opciones"][i] for i in perm],
                    "correcta": perm.index(q["correcta"]),
                }
            )
        if max(Counter(m["correcta"] for m in montadas).values()) <= tope:
            break
    return montadas


def pagina(n: int, titulo: str, v: int, preguntas: list[dict], primera: bool) -> str:
    qs = "\n".join(
        f'  <div class="exam-q">\n    <div class="stem">{i}. {inline(q["pregunta"])}</div>\n'
        + "\n".join(f'    <div class="opt">{LETRAS[k]}) {inline(o)}</div>' for k, o in enumerate(q["opciones"]))
        + "\n  </div>"
        for i, q in enumerate(preguntas, 1)
    )
    return f"""{"" if primera else "---\n"}<!-- _footer: 'Versión {v:02d} · Digitalización · Píldora {n}' -->
<div class="exam-header">
  <h1>Control — Píldora {n}</h1>
  <div class="version">Versión {v:02d}</div>
</div>
<div class="exam-subtitle">{inline(titulo)}</div>
<div class="exam-fields">
  <span>Nombre y apellidos:</span>
  <span>Fecha:</span>
</div>
<div class="exam-instructions">{len(preguntas)} preguntas, una sola opción correcta. Apto con más de 5 aciertos. Rodea la opción elegida.</div>

<div class="exam-questions">
{qs}
</div>

"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argumentos_pildoras(ap)
    ap.add_argument("--versiones", type=int, default=10)
    ap.add_argument("--preguntas", type=int, default=10, help="Preguntas por versión")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    for p in seleccionar(args):
        n = p["n"]
        banco_json = BANCOS / f"{n:02d}.json"
        carpeta = EXAMENES / f"{n:02d}"
        if (carpeta / "versiones.json").exists() and not args.force:
            print(f"Píldora {n}: ya hay exámenes (usa --force).")
            continue
        if not banco_json.exists():
            print(f"Píldora {n}: falta el banco (ejecuta 03_banco.py).")
            continue
        banco = [q for q in json.loads(banco_json.read_text())["preguntas"] if q.get("validada") is not False]
        if len(banco) < args.preguntas:
            print(f"Píldora {n}: el banco solo tiene {len(banco)} preguntas válidas (< {args.preguntas}).")
            continue

        elegidas = elegir_preguntas(banco, args.preguntas, args.versiones, rng)
        versiones = [montar_version(e, rng) for e in elegidas]
        carpeta.mkdir(parents=True, exist_ok=True)

        cabecera = f"---\nmarp: true\ntheme: a4-print\npaginate: false\nbackgroundColor: white\n---\n\n{CSS}\n\n"
        md = cabecera + "".join(
            pagina(n, p["titulo"], v, preguntas, primera=(v == 1)) for v, preguntas in enumerate(versiones, 1)
        )
        examen = carpeta / f"pildora_{n:02d}_examen.md"
        examen.write_text(md)

        cols = " | ".join(str(i) for i in range(1, args.preguntas + 1))
        filas = "\n".join(
            f"| {v:02d} | " + " | ".join(LETRAS[q["correcta"]] for q in preguntas) + " |"
            for v, preguntas in enumerate(versiones, 1)
        )
        (carpeta / f"pildora_{n:02d}_soluciones.md").write_text(
            f"# Píldora {n} — Soluciones\n\n{p['titulo']}\n\n| Versión | {cols} |\n|---|{'---|' * args.preguntas}\n{filas}\n"
        )
        (carpeta / "versiones.json").write_text(
            json.dumps(
                [{"version": v, "preguntas": preguntas} for v, preguntas in enumerate(versiones, 1)],
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )

        uso = Counter(q["id"] for e in elegidas for q in e)
        print(
            f"Píldora {n}: {len(versiones)} versiones de {args.preguntas} (banco {len(banco)}; "
            f"cada pregunta sale entre {min(uso.values())} y {max(uso.values())} veces)"
        )
        if not args.no_pdf:
            if shutil.which("marp"):
                r = subprocess.run(
                    ["marp", "--pdf", str(examen), "-o", str(examen.with_suffix(".pdf")), f"--theme-set={THEMES}"],
                    capture_output=True,
                    text=True,
                )
                print("  PDF OK" if r.returncode == 0 else f"  Error en marp: {r.stderr.strip()[:300]}")
            else:
                print("  (marp no instalado: se omite el PDF)")


if __name__ == "__main__":
    main()
