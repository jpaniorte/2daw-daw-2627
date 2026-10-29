#!/usr/bin/env python3
"""Paso 1: descarga el audio de Drive y lo transcribe, en local (faster-whisper) o con OpenRouter.

    python 01_transcribir.py --pildora 1
    python 01_transcribir.py --all --whisper large-v3-turbo
    python 01_transcribir.py --pildora 1 --motor openrouter --stt-model openai/whisper-large-v3 --sufijo .openrouter

Salida: data/audio/NN/<fichero> y data/transcripciones/NN<sufijo>.txt (se salta lo ya hecho).
Con --motor openrouter el audio se recomprime a mono y se trocea (límite de 60 s por petición del proveedor).
"""

import argparse
import base64
import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from common import AUDIO, OPENROUTER_URL, TRANSCRIPCIONES, argumentos_pildoras, seleccionar

# Términos técnicos que Whisper suele destrozar; se le pasan como contexto inicial.
GLOSARIO = (
    "Píldora de informática: CPU, ALU, unidad de control, registros, bus, DMA, RAM, ROM, caché, "
    "microprocesador, SGBD, SQL, modelo relacional, TCP/IP, UML, POO, hardware, software, bit, byte, "
    "ASCII, Unicode, complemento a dos, sistema operativo, kernel."
)


def descargar(p: dict):
    destino = AUDIO / f"{p['n']:02d}"
    existentes = [f for f in destino.glob("*") if f.is_file()] if destino.is_dir() else []
    if existentes:
        return existentes[0]
    import gdown

    destino.mkdir(parents=True, exist_ok=True)
    print(f"  Descargando audio de Drive ({p['drive_id']})...")
    ruta = gdown.download(id=p["drive_id"], output=str(destino) + "/", quiet=False)
    if not ruta:
        raise SystemExit(f"No se pudo descargar la píldora {p['n']} (¿el fichero es público?)")
    return destino / ruta.rsplit("/", 1)[-1]


def transcribir(modelo, audio) -> str:
    segmentos, info = modelo.transcribe(
        str(audio),
        language="es",
        vad_filter=True,
        beam_size=5,
        initial_prompt=GLOSARIO,
    )
    print(f"  Duración: {info.duration / 60:.1f} min")
    parrafos, actual, fin_previo, minuto = [], [], 0.0, 0
    for s in segmentos:
        if int(s.end // 60) > minuto:  # progreso: una línea por minuto de audio procesado
            minuto = int(s.end // 60)
            print(f"  {minuto}/{info.duration / 60:.0f} min de audio transcritos", flush=True)
        if actual and s.start - fin_previo > 1.5:  # pausa larga -> párrafo nuevo
            parrafos.append(" ".join(actual))
            actual = []
        actual.append(s.text.strip())
        fin_previo = s.end
    if actual:
        parrafos.append(" ".join(actual))
    return "\n\n".join(parrafos) + "\n"


def trocear(audio: Path, destino: Path, segundos: int) -> list[Path]:
    """Recomprime a mono 16 kHz / 48 kbps (voz) y lo parte en trozos de `segundos`."""
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k",
         "-f", "segment", "-segment_time", str(segundos), "-reset_timestamps", "1", str(destino / "trozo_%03d.mp3")],
        check=True,
    )
    return sorted(destino.glob("trozo_*.mp3"))


def transcribir_trozo(modelo: str, trozo: Path, reintentos: int = 3) -> dict:
    cuerpo = json.dumps({
        "model": modelo,
        "language": "es",
        "input_audio": {"data": base64.b64encode(trozo.read_bytes()).decode(), "format": "mp3"},
    }).encode()
    req = urllib.request.Request(
        f"{OPENROUTER_URL}/audio/transcriptions",
        data=cuerpo,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"},
    )
    for intento in range(1, reintentos + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            detalle = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503, 504, 524, 529) and intento < reintentos:
                print(f"    HTTP {e.code}; reintento {intento}/{reintentos - 1}...", flush=True)
                time.sleep(3 * intento)
                continue
            raise SystemExit(f"Error de OpenRouter (HTTP {e.code}): {detalle}")


def transcribir_openrouter(modelo: str, audio: Path, segundos: int) -> str:
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise SystemExit("Falta OPENROUTER_API_KEY (ver .env.example)")
    textos, coste, duracion = [], 0.0, 0.0
    with tempfile.TemporaryDirectory() as tmp:
        trozos = trocear(audio, Path(tmp), segundos)
        print(f"  {len(trozos)} trozos de ~{segundos // 60} min; modelo {modelo}", flush=True)
        for i, t in enumerate(trozos, 1):
            r = transcribir_trozo(modelo, t)
            u = r.get("usage") or {}
            coste += u.get("cost") or 0.0
            duracion += u.get("seconds") or 0.0
            textos.append(r["text"].strip())
            print(f"  trozo {i}/{len(trozos)} OK ({len(r['text'].split())} palabras)", flush=True)
    print(f"  Coste total: {coste:.4f} $ por {duracion / 60:.1f} min de audio", flush=True)
    return "\n\n".join(textos) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argumentos_pildoras(ap)
    ap.add_argument("--whisper", default="large-v3", help="Modelo local (small, medium, large-v3, large-v3-turbo...)")
    ap.add_argument("--motor", choices=["local", "openrouter"], default="local")
    ap.add_argument(
        "--stt-model",
        default=os.environ.get("OPENROUTER_STT_MODEL", "openai/whisper-large-v3"),
        help="Modelo STT de OpenRouter (ver: python common.py --list-models --stt)",
    )
    ap.add_argument("--trozo", type=int, default=240, help="Segundos por trozo con --motor openrouter (def. 240)")
    ap.add_argument("--sufijo", default="", help="Sufijo del fichero de salida, p. ej. .openrouter (para comparar motores)")
    args = ap.parse_args()

    def salida(p):
        return TRANSCRIPCIONES / f"{p['n']:02d}{args.sufijo}.txt"

    pendientes = [p for p in seleccionar(args) if args.force or not salida(p).exists()]
    if not pendientes:
        print("Nada que transcribir (usa --force para rehacer).")
        return
    TRANSCRIPCIONES.mkdir(parents=True, exist_ok=True)

    modelo = None
    if args.motor == "local":
        from faster_whisper import WhisperModel

        print(f"Cargando Whisper '{args.whisper}' (la primera vez descarga el modelo)...")
        modelo = WhisperModel(args.whisper, device="cpu", compute_type="int8")
    for p in pendientes:
        print(f"Píldora {p['n']}: {p['titulo'][:60]}")
        audio = descargar(p)
        if args.motor == "local":
            texto = transcribir(modelo, audio)
        else:
            texto = transcribir_openrouter(args.stt_model, audio, args.trozo)
        salida(p).write_text(texto)
        print(f"  OK -> transcripciones/{salida(p).name} ({len(texto.split())} palabras)")


if __name__ == "__main__":
    main()
