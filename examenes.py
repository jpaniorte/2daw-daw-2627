#!/usr/bin/env python3
"""Genera el examen (20 versiones) y su solucionario de un bloque a partir de su banco de test.

Uso:
    python3 examenes.py "UD2/2.1 Fundamentos web" web_1 --titulo "web bloque 2.1: Fundamentos web" --pie "UD2: Arquitecturas Web"

Lee <prefijo>_test.md (banco de preguntas) y <prefijo>_test_sol.md (soluciones) de la carpeta del bloque y escribe:
    <prefijo>_examen.md      Marp (tema a4-print): N versiones de P preguntas, 2 páginas A4 cada una
    <prefijo>_examen_sol.md  Marp: tablas "letra correcta (#nº en el banco)" de cada versión
    pdf/<prefijo>_examen.pdf y pdf/<prefijo>_examen_sol.pdf   (si marp está instalado)

Como en Git y Docker, las opciones NO se barajan: solo cambia qué preguntas salen y en qué orden. Cada pregunta del
banco aparece el mismo número de veces (versiones x preguntas / tamaño del banco). Los .md y los PDF de examen
están ignorados por git (ver .gitignore).
"""

import argparse
import html
import random
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_DIR = BASE_DIR / "themes"
LETRAS = "ABCD"
INSTRUCCION = "Rodea con un círculo la única opción correcta en cada pregunta."

PREGUNTA_RE = re.compile(r"^\*\*(\d+)\.\*\*\s*(.*?)\n\n((?:- [A-D]\) .*\n?)+)", re.M)
SOLUCION_RE = re.compile(r"^\*\*(\d+)\. ([A-D])\)\*\*", re.M)

CSS = """<style>
section { place-content: flex-start !important; }
.exam-header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #333; padding-bottom: 6px; margin-bottom: 6px; }
.exam-header h1 { font-size: 18px; margin: 0; }
.exam-header .version { font-size: 16px; font-weight: 700; }
.exam-fields { display: flex; gap: 24px; font-size: 12px; margin-bottom: 8px; }
.exam-fields span { border-bottom: 1px solid #888; padding-bottom: 2px; flex: 1; }
.exam-instructions { font-size: 11px; color: #444; margin-bottom: 8px; }
.exam-questions { columns: 2; column-gap: 10mm; font-size: 11px; line-height: 1.25; }
.exam-q { break-inside: avoid; margin-bottom: 7px; }
.exam-q .stem { font-weight: 600; margin-bottom: 2px; }
.exam-q .opt { margin-left: 4px; }
.exam-back-title { font-size: 13px; font-weight: 700; margin-bottom: 6px; }
.exam-q code, .exam-header code { background: #eef0f4; border-radius: 3px; padding: 0 3px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
</style>"""


def inline(texto: str) -> str:
    """Markdown en línea (`código`, **negrita**, *cursiva*) a HTML: dentro de un <div> Marp no lo interpreta."""
    partes = re.split(r"(`[^`]+`)", texto)
    salida = []
    for parte in partes:
        if parte.startswith("`") and parte.endswith("`") and len(parte) > 1:
            salida.append(f"<code>{html.escape(parte[1:-1], quote=False)}</code>")
        else:
            h = html.escape(parte, quote=False)
            h = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", h)
            h = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", h)
            salida.append(h)
    return "".join(salida)


def leer_banco(carpeta: Path, prefijo: str) -> list[dict]:
    test = (carpeta / f"{prefijo}_test.md").read_text()
    sol = (carpeta / f"{prefijo}_test_sol.md").read_text()
    letras = {int(n): l for n, l in SOLUCION_RE.findall(sol)}
    banco = []
    for m in PREGUNTA_RE.finditer(test):
        n = int(m.group(1))
        opciones = [re.sub(r"^- [A-D]\) ", "", l).strip() for l in m.group(3).strip().split("\n")]
        if len(opciones) != 4:
            sys.exit(f"La pregunta {n} no tiene 4 opciones")
        if n not in letras:
            sys.exit(f"La pregunta {n} no tiene solución en {prefijo}_test_sol.md")
        banco.append({
            "n": n,
            "pregunta": re.sub(r"\s+", " ", m.group(2)).strip(),
            "opciones": opciones,
            "correcta": LETRAS.index(letras[n]),
        })
    if [q["n"] for q in banco] != list(range(1, len(banco) + 1)):
        sys.exit("La numeración de las preguntas del banco no es 1..N continua")
    if len(letras) != len(banco):
        sys.exit(f"Hay {len(banco)} preguntas pero {len(letras)} soluciones")
    return banco


def repartir(banco: list[dict], versiones: int, preguntas: int, rng: random.Random) -> list[list[dict]]:
    """Cada permutación del banco se corta en bloques de `preguntas`: sin repetidas dentro de una versión
    y todas las preguntas con las mismas apariciones. Se reintenta si una letra queda muy desequilibrada."""
    if len(banco) % preguntas:
        sys.exit(f"El banco ({len(banco)}) debe ser múltiplo de las preguntas por versión ({preguntas})")
    por_perm = len(banco) // preguntas
    if versiones % por_perm:
        sys.exit(f"Las versiones ({versiones}) deben ser múltiplo de {por_perm} (bloques por permutación)")
    minimo, maximo = preguntas // 4 - 2, -(-preguntas // 4) + 2  # p. ej. 20 preguntas -> 3..7 por letra
    resultado = []
    for _ in range(versiones // por_perm):
        for _ in range(2000):
            perm = banco[:]
            rng.shuffle(perm)
            bloques = [perm[i : i + preguntas] for i in range(0, len(perm), preguntas)]
            cuentas = [Counter(q["correcta"] for q in b) for b in bloques]
            if all(minimo <= c.get(k, 0) <= maximo for c in cuentas for k in range(4)):
                break
        resultado += bloques
    return resultado


def pagina(titulo: str, pie: str, v: int, preguntas: list[dict], primera: bool, inicio: int, total: int) -> str:
    qs = "\n".join(
        f'  <div class="exam-q">\n    <div class="stem">{inicio + i}. {inline(q["pregunta"])}</div>\n'
        + "\n".join(f'    <div class="opt">{LETRAS[k]}) {inline(o)}</div>' for k, o in enumerate(q["opciones"]))
        + "\n  </div>"
        for i, q in enumerate(preguntas)
    )
    pag = 1 if primera else 2
    cabecera = (
        f'<div class="exam-header">\n  <h1>Examen — {inline(titulo)}</h1>\n  <div class="version">Versión {v:02d}</div>\n</div>\n'
        '<div class="exam-fields">\n  <span>Nombre y apellidos:</span>\n  <span>Fecha:</span>\n</div>\n'
        f'<div class="exam-instructions">{INSTRUCCION}</div>\n'
        if primera
        else f'<div class="exam-back-title">Versión {v:02d} (continuación)</div>\n'
    )
    sep = "" if (primera and v == 1) else "---\n"
    return (
        f"{sep}<!-- _footer: 'Versión {v:02d} · Página {pag}/2 · Despliegue de Aplicaciones Web (0614) · {pie}' -->\n"
        f'{cabecera}\n<div class="exam-questions">\n{qs}\n</div>\n\n'
    )


def montar_examen(titulo: str, pie: str, versiones: list[list[dict]]) -> str:
    cab = (
        f"---\nmarp: true\ntheme: a4-print\npaginate: false\nbackgroundColor: white\nfooter: 'Despliegue de Aplicaciones Web (0614) · {pie}'\n---\n\n{CSS}\n\n"
    )
    cuerpo = ""
    for v, preguntas in enumerate(versiones, 1):
        mitad = len(preguntas) // 2
        cuerpo += pagina(titulo, pie, v, preguntas[:mitad], True, 1, len(preguntas))
        cuerpo += pagina(titulo, pie, v, preguntas[mitad:], False, mitad + 1, len(preguntas))
    return cab + cuerpo


def montar_soluciones(titulo: str, pie: str, prefijo: str, versiones: list[list[dict]]) -> str:
    corto = titulo.split(":")[0].strip()
    cabecera = f"---\nmarp: true\ntheme: a4-print\npaginate: true\nbackgroundColor: white\nfooter: 'Despliegue de Aplicaciones Web (0614) · {pie}'\n---\n\n"
    partes = [
        f"<!-- _class: lead -->\n# {corto}\n## Soluciones de `{prefijo}_examen.md` (uso del profesor)\n\n"
        f"{len(versiones)} versiones · clave de respuestas + nº de pregunta original en `{prefijo}_test.md`\n",
    ]
    for i in range(0, len(versiones), 5):
        grupo = versiones[i : i + 5]
        nums = ", ".join(f"{i + k + 1:02d}" for k in range(len(grupo)))
        filas = "\n".join(
            f"| {p + 1} | " + " | ".join(f"{LETRAS[g[p]['correcta']]} (#{g[p]['n']})" for g in grupo) + " |"
            for p in range(len(grupo[0]))
        )
        cab = "| Preg. | " + " | ".join(f"V{i + k + 1:02d}" for k in range(len(grupo))) + " |"
        partes.append(f"## Soluciones — versiones {nums}\n\n{cab}\n| --- |{' --- |' * len(grupo)}\n{filas}\n")
    return cabecera + "\n---\n\n".join(partes)


def pdf(md: Path, destino: Path) -> None:
    destino.parent.mkdir(exist_ok=True)
    comando = ["marp", "--pdf", str(md), "-o", str(destino)]
    if THEMES_DIR.is_dir():
        comando.append(f"--theme-set={THEMES_DIR}")
    r = subprocess.run(comando, capture_output=True, text=True)
    print(f"  OK -> {destino.relative_to(md.parent)}" if r.returncode == 0 else f"  Error en marp: {r.stderr.strip()[:300]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpeta", help='Carpeta del bloque, p. ej. "UD2/2.1 Fundamentos web"')
    ap.add_argument("prefijo", help="Prefijo de los ficheros, p. ej. web_1")
    ap.add_argument("--titulo", required=True, help='Título corto, p. ej. "web bloque 2.1: Fundamentos web"')
    ap.add_argument("--pie", required=True, help='Pie de página, p. ej. "UD2: Arquitecturas Web"')
    ap.add_argument("--versiones", type=int, default=20)
    ap.add_argument("--preguntas", type=int, default=20, help="Preguntas por versión (par: mitad en cada página)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    if a.preguntas % 2:
        sys.exit("--preguntas debe ser par (se reparten en 2 páginas)")
    carpeta = (BASE_DIR / a.carpeta) if not Path(a.carpeta).is_absolute() else Path(a.carpeta)
    banco = leer_banco(carpeta, a.prefijo)
    versiones = repartir(banco, a.versiones, a.preguntas, random.Random(a.seed))
    apariciones = Counter(q["n"] for v in versiones for q in v)
    print(f"Banco de {len(banco)} preguntas -> {len(versiones)} versiones de {a.preguntas} "
          f"(cada pregunta sale {min(apariciones.values())}-{max(apariciones.values())} veces)")

    examen, sol = carpeta / f"{a.prefijo}_examen.md", carpeta / f"{a.prefijo}_examen_sol.md"
    examen.write_text(montar_examen(a.titulo, a.pie, versiones))
    sol.write_text(montar_soluciones(a.titulo, a.pie, a.prefijo, versiones))
    print(f"  OK -> {examen.name}, {sol.name}")
    if a.no_pdf:
        return
    if not shutil.which("marp"):
        print("  (marp no instalado: se omiten los PDF)")
        return
    pdf(examen, carpeta / "pdf" / f"{a.prefijo}_examen.pdf")
    pdf(sol, carpeta / "pdf" / f"{a.prefijo}_examen_sol.pdf")


if __name__ == "__main__":
    main()
