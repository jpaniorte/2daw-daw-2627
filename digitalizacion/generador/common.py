#!/usr/bin/env python3
"""Utilidades compartidas por los scripts del generador de píldoras.

Uso suelto:
    python common.py --list-models [filtro]   Lista los modelos de OpenRouter (ID y precio por 1M tokens)
    python common.py --list-models --stt      Lista los modelos de transcripción de audio (precio por hora de audio)
    python common.py --pildoras               Lista las píldoras con audio que detecta en pildoras.md
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PILDORAS_MD = ROOT.parent / "pildoras.md"
DATA = ROOT / "data"
AUDIO = DATA / "audio"
TRANSCRIPCIONES = DATA / "transcripciones"
DOSIERES = DATA / "dosieres"
BANCOS = DATA / "bancos"
EXAMENES = DATA / "examenes"

OPENROUTER_URL = "https://openrouter.ai/api/v1"

FILA_RE = re.compile(
    r"<td>(\d+)</td><td>(.*?)</td><td class=\"pildora-reproductor\">(.*?)</td>", re.S
)
DRIVE_RE = re.compile(r"/file/d/([\w-]+)")


def cargar_env() -> None:
    """Lee generador/.env (CLAVE=valor) sin pisar variables ya definidas."""
    env = ROOT / ".env"
    if not env.is_file():
        return
    for linea in env.read_text().splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip("\"'"))


cargar_env()


def leer_pildoras() -> dict[int, dict]:
    """Devuelve {nº: {"n", "titulo", "drive_id"}} solo de las píldoras que ya tienen audio."""
    resultado = {}
    for n, titulo, reproductor in FILA_RE.findall(PILDORAS_MD.read_text()):
        m = DRIVE_RE.search(reproductor)
        if m:
            resultado[int(n)] = {
                "n": int(n),
                "titulo": html.unescape(re.sub(r"<[^>]+>", "", titulo)).strip(),
                "drive_id": m.group(1),
            }
    return resultado


def argumentos_pildoras(parser: argparse.ArgumentParser) -> None:
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--pildora", "-p", type=int, nargs="+", metavar="N", help="Número(s) de píldora")
    g.add_argument("--all", action="store_true", help="Todas las píldoras con audio")
    parser.add_argument("--force", action="store_true", help="Rehacer aunque ya exista la salida")


def seleccionar(args) -> list[dict]:
    todas = leer_pildoras()
    if args.all:
        return [todas[n] for n in sorted(todas)]
    faltan = [n for n in args.pildora if n not in todas]
    if faltan:
        sys.exit(f"Sin audio en pildoras.md: {faltan}. Con audio: {sorted(todas)}")
    return [todas[n] for n in args.pildora]


def argumento_modelo(parser: argparse.ArgumentParser, nombre="--model", env="OPENROUTER_MODEL") -> None:
    parser.add_argument(
        nombre,
        default=os.environ.get(env),
        help=f"ID de modelo de OpenRouter (por defecto ${env}). Ver: python common.py --list-models",
    )


def cliente():
    clave = os.environ.get("OPENROUTER_API_KEY")
    if not clave:
        sys.exit("Falta OPENROUTER_API_KEY (ponla en generador/.env, ver .env.example)")
    from openai import OpenAI

    return OpenAI(base_url=OPENROUTER_URL, api_key=clave)


def chat(
    modelo: str, system: str, user: str, temperature: float = 0.3, reintentos: int = 3, razonar: bool = False
) -> str:
    """Una llamada de chat a OpenRouter.

    Por defecto se APAGA el razonamiento: los modelos de razonamiento (DeepSeek v4.1 flash, GPT-6 Luna...) gastan
    muchísimos tokens ocultos que se cobran como salida, y a veces agotan el presupuesto sin escribir respuesta
    ("respuesta vacía"). Las tareas de este generador no lo necesitan.
    """
    if not modelo:
        sys.exit("Falta el modelo: usa --model o define OPENROUTER_MODEL")
    c = cliente()
    for intento in range(1, reintentos + 1):
        try:
            r = c.chat.completions.create(
                model=modelo,
                temperature=temperature,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                extra_body=None if razonar else {"reasoning": {"enabled": False}},
            )
            texto = r.choices[0].message.content
            if texto:
                return texto
            raise RuntimeError("respuesta vacía")
        except Exception as e:  # noqa: BLE001 - reintento genérico ante fallos de red/API
            if intento == reintentos:
                raise
            espera = 2**intento
            print(f"  Error ({e}); reintento {intento}/{reintentos - 1} en {espera}s...")
            time.sleep(espera)


def extraer_json(texto: str):
    """Extrae el primer JSON de una respuesta, aunque venga dentro de un bloque ```json."""
    m = re.search(r"```(?:json)?\s*(.*?)```", texto, re.S)
    if m:
        texto = m.group(1)
    inicio = min((i for i in (texto.find("["), texto.find("{")) if i != -1), default=-1)
    if inicio == -1:
        raise ValueError("la respuesta no contiene JSON")
    return json.loads(texto[inicio:])


def listar_modelos(filtro: str = "", stt: bool = False) -> None:
    """Lista modelos de texto (precio por 1M tokens) o, con stt=True, de transcripción (precio por hora)."""
    url = f"{OPENROUTER_URL}/models" + ("?output_modalities=transcription" if stt else "")
    with urllib.request.urlopen(url, timeout=30) as r:
        modelos = json.load(r)["data"]
    filas = []
    for m in modelos:
        if filtro.lower() not in m["id"].lower():
            continue
        p = m.get("pricing", {})
        try:
            entrada, salida = float(p.get("prompt", 0)), float(p.get("completion", 0))
        except (TypeError, ValueError):
            entrada = salida = float("nan")
        if stt:
            # Los modelos ASR cobran por segundo de audio; los basados en tokens (completion > 0) van aparte.
            por_tokens = salida > 0
            filas.append((m["id"], entrada * (1e6 if por_tokens else 3600), "tokens" if por_tokens else "$/hora"))
        else:
            filas.append((m["id"], entrada * 1e6, salida * 1e6, m.get("context_length", 0)))
    if stt:
        print(f"{'ID':58} {'precio':>9}  unidad")
        for id_, precio, unidad in sorted(filas, key=lambda f: (f[2] != "$/hora", f[1])):
            print(f"{id_:58} {precio:9.3f}  {unidad if unidad == '$/hora' else '$/1M tokens de entrada (aparte)'}")
    else:
        print(f"{'ID':60} {'$/1M in':>9} {'$/1M out':>9} {'contexto':>9}")
        for id_, i, o, ctx in sorted(filas):
            print(f"{id_:60} {i:9.2f} {o:9.2f} {ctx:9}")
    print(f"\n{len(filas)} modelos")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list-models", nargs="?", const="", metavar="FILTRO")
    p.add_argument("--stt", action="store_true", help="con --list-models: solo modelos de transcripción")
    p.add_argument("--pildoras", action="store_true")
    a = p.parse_args()
    if a.list_models is not None:
        listar_modelos(a.list_models, a.stt)
    elif a.pildoras:
        for n, d in sorted(leer_pildoras().items()):
            print(f"{n:3}  {d['drive_id']}  {d['titulo'][:70]}")
    else:
        p.print_help()
