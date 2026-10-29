#!/usr/bin/env python3
"""Paso 2: convierte la transcripción en un dosier de estudio con un modelo de OpenRouter.

    python 02_dosier.py --pildora 1 --model <id>
    python 02_dosier.py --all

Salida: data/dosieres/NN.md. Es el punto de revisión humana: léelo antes de generar preguntas.
"""

import argparse

from common import DOSIERES, TRANSCRIPCIONES, argumento_modelo, argumentos_pildoras, chat, seleccionar

SYSTEM = """Eres un profesor que prepara material de estudio en español a partir de la transcripción de un audio.
Reglas estrictas:
- Usa SOLO lo que aparece en la transcripción. No añadas datos, ejemplos, cifras ni definiciones de tu cosecha:
  los alumnos solo han escuchado ese audio y se les va a examinar de él.
- Corrige los errores evidentes de transcripción en términos técnicos, sin cambiar el significado.
- Si algo del audio es ambiguo o parece un error del locutor, no lo "arregles": déjalo como se dice.
- Elimina muletillas y repeticiones, y reorganiza para que se estudie bien.
Formato Markdown: un título H1 con el de la píldora; secciones H2/H3 por tema; definiciones en negrita;
listas para enumeraciones; tablas para comparativas; y al final "## Conceptos clave" con una lista de
término: definición breve, y "## Resumen" de 5-8 líneas."""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argumentos_pildoras(ap)
    argumento_modelo(ap)
    args = ap.parse_args()

    DOSIERES.mkdir(parents=True, exist_ok=True)
    for p in seleccionar(args):
        salida = DOSIERES / f"{p['n']:02d}.md"
        trans = TRANSCRIPCIONES / f"{p['n']:02d}.txt"
        if salida.exists() and not args.force:
            print(f"Píldora {p['n']}: ya existe el dosier (usa --force).")
            continue
        if not trans.exists():
            print(f"Píldora {p['n']}: falta la transcripción (ejecuta 01_transcribir.py).")
            continue
        print(f"Píldora {p['n']}: generando dosier con {args.model}...")
        user = f"Título de la píldora: {p['titulo']}\n\nTranscripción:\n\n{trans.read_text()}"
        salida.write_text(chat(args.model, SYSTEM, user, temperature=0.2).strip() + "\n")
        print(f"  OK -> dosieres/{p['n']:02d}.md")


if __name__ == "__main__":
    main()
