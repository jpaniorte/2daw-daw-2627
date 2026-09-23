#!/usr/bin/env python3
"""Genera PDF y PPTX a partir de ficheros Markdown usando Marp CLI.

Uso:
    python3 build.py all              Genera PDF y PPTX de los .md que aún no tengan salida generada
    python3 build.py fichero.md       Genera PDF y PPTX de ese fichero solo si no existen ya
    python3 build.py rebuild all      Regenera PDF y PPTX de todos los .md, existan o no
    python3 build.py rebuild fichero.md   Regenera PDF y PPTX de ese fichero, exista o no
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_DIR = BASE_DIR / "themes"


def marp_disponible() -> bool:
    return subprocess.run(
        ["marp", "--version"], capture_output=True
    ).returncode == 0


def construir(md_path: Path, forzar: bool = False) -> None:
    pdf_path = md_path.parent / "pdf" / md_path.with_suffix(".pdf").name
    pptx_path = md_path.parent / "pptx" / md_path.with_suffix(".pptx").name

    for destino, flag in ((pdf_path, "--pdf"), (pptx_path, "--pptx")):
        if not forzar and destino.exists():
            print(f"  Ya existe {destino.parent.name}/{destino.name}, se omite.")
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        print(f"Generando {destino.parent.name}/{destino.name}...")
        comando = ["marp", flag, str(md_path), "-o", str(destino)]
        if THEMES_DIR.is_dir():
            # Registra los temas compartidos (p.ej. "a4-print" para documentos
            # imprimibles) para cualquier .md que los referencie con `theme:`.
            comando.append(f"--theme-set={THEMES_DIR}")
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
        )
        if resultado.returncode != 0:
            print(f"  Error generando {destino.parent.name}/{destino.name}:")
            print(resultado.stderr.strip())
        else:
            print(f"  OK -> {destino.parent.name}/{destino.name}")


def main() -> None:
    argumentos = sys.argv[1:]

    forzar = False
    if argumentos and argumentos[0] == "rebuild":
        forzar = True
        argumentos = argumentos[1:]

    if len(argumentos) != 1:
        print(__doc__)
        sys.exit(1)

    if not marp_disponible():
        print("Error: no se encuentra 'marp' en el PATH. Instálalo con: npm install -g @marp-team/marp-cli")
        sys.exit(1)

    argumento = argumentos[0]

    if argumento == "all":
        ficheros_md = sorted(
            p for p in BASE_DIR.rglob("*.md")
            if not any(
                parte.startswith(".") or parte in ("pdf", "pptx", "themes")
                for parte in p.relative_to(BASE_DIR).parts
            )
        )
        if not ficheros_md:
            print("No se han encontrado ficheros .md en el directorio ni en sus subcarpetas.")
            sys.exit(0)
    else:
        md_path = Path(argumento)
        if not md_path.is_absolute():
            md_path = BASE_DIR / md_path
        if not md_path.exists():
            print(f"Error: el fichero '{argumento}' no existe.")
            sys.exit(1)
        if md_path.suffix.lower() != ".md":
            print(f"Error: '{argumento}' no es un fichero .md.")
            sys.exit(1)
        ficheros_md = [md_path]

    for md_path in ficheros_md:
        print(f"\n== {md_path.name} ==")
        construir(md_path, forzar=forzar)


if __name__ == "__main__":
    main()
