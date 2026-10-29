#!/usr/bin/env python3
"""Paso 3: genera el banco de preguntas de cada píldora a partir de su dosier y lo valida con otro modelo.

    python 03_banco.py --pildora 1 --model <generador> --validator-model <otro-modelo>
    python 03_banco.py --all --preguntas 40

El validador responde a ciegas (sin ver la clave) usando el dosier; las preguntas en las que discrepa
con la clave se descartan. Salida: data/bancos/NN.json
"""

import argparse
import json
import os
import random
import re

from common import (
    BANCOS,
    DOSIERES,
    argumento_modelo,
    argumentos_pildoras,
    chat,
    extraer_json,
    seleccionar,
)

LETRAS = "ABCD"
# Opciones que dejan de tener sentido al barajar
PROHIBIDAS = re.compile(r"\b(todas|ninguna)\b.*\banteriores\b|\bambas\b|\b[ABCD]\s*(y|e|o)\s*[ABCD]\b", re.I)

SYSTEM_GEN = """Eres un profesor que redacta preguntas tipo test en español para un control de una píldora de informática.
Reglas:
- Basa TODAS las preguntas exclusivamente en el dosier. No preguntes nada que no esté en él.
- Cada pregunta: enunciado claro, 4 opciones, UNA sola correcta y 3 distractores plausibles (errores o
  confusiones típicas, no absurdos). Opciones de longitud parecida; la correcta no debe ser la más larga.
- Evita "todas las anteriores", "ninguna de las anteriores", "A y B" y negaciones dobles.
- Cubre todo el dosier de forma repartida y no repitas el mismo concepto en dos preguntas. Mezcla
  definiciones, diferencias entre conceptos y casos de aplicación.
- "cita": copia literal, breve, del dosier que justifica la respuesta correcta.
Responde SOLO con un array JSON, sin texto alrededor:
[{"pregunta": "...", "opciones": ["...", "...", "...", "..."], "correcta": 0, "cita": "..."}]
donde "correcta" es el índice (0-3) de la opción correcta."""

SYSTEM_VAL = """Eres un alumno atento que responde un test usando EXCLUSIVAMENTE el dosier dado.
Para cada pregunta elige la opción que mejor se ajusta al dosier. Si ninguna encaja o hay más de una
válida, responde "?".
Responde SOLO con un array JSON: [{"n": 1, "respuesta": "B"}, ...]"""


def validar_estructura(q: dict) -> str | None:
    if not isinstance(q.get("pregunta"), str) or not q["pregunta"].strip():
        return "sin enunciado"
    ops = q.get("opciones")
    if not (isinstance(ops, list) and len(ops) == 4 and all(isinstance(o, str) and o.strip() for o in ops)):
        return "no tiene 4 opciones"
    if len({o.strip().lower() for o in ops}) != 4:
        return "opciones repetidas"
    if q.get("correcta") not in (0, 1, 2, 3):
        return "índice de correcta inválido"
    if any(PROHIBIDAS.search(o) for o in ops):
        return "opción dependiente de otras"
    return None


def equilibrar(preguntas: list[dict], rng: random.Random) -> None:
    """Coloca la correcta en A/B/C/D de forma repartida (intercambia con la opción que ocupaba ese hueco)."""
    destinos = []
    while len(destinos) < len(preguntas):
        bloque = [0, 1, 2, 3]
        rng.shuffle(bloque)
        destinos += bloque
    for q, d in zip(preguntas, destinos):
        o, c = q["opciones"], q["correcta"]
        o[c], o[d] = o[d], o[c]
        q["correcta"] = d


def formatear(preguntas: list[dict]) -> str:
    bloques = []
    for i, q in enumerate(preguntas, 1):
        ops = "\n".join(f"{LETRAS[k]}) {o}" for k, o in enumerate(q["opciones"]))
        bloques.append(f"{i}. {q['pregunta']}\n{ops}")
    return "\n\n".join(bloques)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argumentos_pildoras(ap)
    argumento_modelo(ap)
    argumento_modelo(ap, "--validator-model", "OPENROUTER_VALIDATOR_MODEL")
    ap.add_argument("--preguntas", type=int, default=40, help="Preguntas a generar por píldora (def. 40)")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    if not args.validator_model:
        print("AVISO: sin --validator-model no se validan las preguntas (recomendado usar otro modelo).")
    if args.validator_model and args.validator_model == args.model:
        print("AVISO: el validador es el mismo modelo que el generador; mejor uno de otra familia.")

    BANCOS.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    for p in seleccionar(args):
        salida = BANCOS / f"{p['n']:02d}.json"
        dosier = DOSIERES / f"{p['n']:02d}.md"
        if salida.exists() and not args.force:
            print(f"Píldora {p['n']}: ya existe el banco (usa --force).")
            continue
        if not dosier.exists():
            print(f"Píldora {p['n']}: falta el dosier (ejecuta 02_dosier.py).")
            continue

        print(f"Píldora {p['n']}: generando {args.preguntas} preguntas con {args.model}...")
        bruto = extraer_json(
            chat(
                args.model,
                SYSTEM_GEN,
                f"Genera {args.preguntas} preguntas.\n\nDosier:\n\n{dosier.read_text()}",
                temperature=0.5,
            )
        )
        descartadas, validas = [], []
        for q in bruto:
            motivo = validar_estructura(q)
            if motivo:
                descartadas.append({**q, "motivo": motivo})
            else:
                validas.append({k: q.get(k) for k in ("pregunta", "opciones", "correcta", "cita")})
        equilibrar(validas, rng)

        if args.validator_model and validas:
            print(f"  Validando {len(validas)} preguntas con {args.validator_model}...")
            resp = extraer_json(
                chat(
                    args.validator_model,
                    SYSTEM_VAL,
                    f"Dosier:\n\n{dosier.read_text()}\n\nPreguntas:\n\n{formatear(validas)}",
                    temperature=0,
                )
            )
            dadas = {int(r["n"]): str(r["respuesta"]).strip().upper()[:1] for r in resp if "n" in r}
            for i, q in enumerate(validas, 1):
                q["validada"] = dadas.get(i) == LETRAS[q["correcta"]]
                if not q["validada"]:
                    q["motivo"] = f"el validador respondió {dadas.get(i, 'nada')} y la clave es {LETRAS[q['correcta']]}"
        else:
            for q in validas:
                q["validada"] = None

        buenas = [q for q in validas if q["validada"] is not False]
        for i, q in enumerate(validas, 1):
            q["id"] = i
        descartadas += [q for q in validas if q["validada"] is False]
        reparto = {L: sum(1 for q in buenas if LETRAS[q["correcta"]] == L) for L in LETRAS}
        salida.write_text(
            json.dumps(
                {
                    "pildora": p["n"],
                    "titulo": p["titulo"],
                    "modelo": args.model,
                    "validador": args.validator_model,
                    "preguntas": validas,
                    "descartadas": [q for q in descartadas if q.get("validada") is not False],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        print(f"  OK -> bancos/{p['n']:02d}.json: {len(buenas)} válidas, {len(descartadas)} descartadas, correctas {reparto}")


if __name__ == "__main__":
    main()
