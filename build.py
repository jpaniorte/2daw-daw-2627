#!/usr/bin/env python3
"""Genera PDF y PPTX a partir de ficheros Markdown usando Marp CLI.

Uso:
    python3 build.py all              Genera PDF y PPTX de todos los .md del directorio
    python3 build.py fichero.md       Genera PDF y PPTX solo de ese fichero
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def marp_disponible() -> bool:
    return subprocess.run(
        ["marp", "--version"], capture_output=True
    ).returncode == 0


def construir(md_path: Path) -> None:
    pdf_path = md_path.with_suffix(".pdf")
    pptx_path = md_path.with_suffix(".pptx")

    for destino, flag in ((pdf_path, "--pdf"), (pptx_path, "--pptx")):
        print(f"Generando {destino.name}...")
        resultado = subprocess.run(
            ["marp", flag, str(md_path), "-o", str(destino)],
            capture_output=True,
            text=True,
        )
        if resultado.returncode != 0:
            print(f"  Error generando {destino.name}:")
            print(resultado.stderr.strip())
        else:
            print(f"  OK -> {destino.name}")


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    if not marp_disponible():
        print("Error: no se encuentra 'marp' en el PATH. Instálalo con: npm install -g @marp-team/marp-cli")
        sys.exit(1)

    argumento = sys.argv[1]

    if argumento == "all":
        ficheros_md = sorted(BASE_DIR.glob("*.md"))
        if not ficheros_md:
            print("No se han encontrado ficheros .md en el directorio.")
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
        construir(md_path)


if __name__ == "__main__":
    main()
