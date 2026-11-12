#!/bin/zsh
# Flujo completo de las píldoras: PDF -> audio (Gemini Notebook) -> mp3 -> Drive -> pildoras.md
#                                  -> transcripción -> dosier -> banco de preguntas -> exámenes.
#
# Uso: ./pildoras.sh [N ...] [--max K] [--dry-run] [--login] [--commit] [--solo-audio] [--sin-audio]
#   Los PDF van en pdf/N.pdf. Sin N procesa todas las pendientes.
#   Es idempotente: salta lo ya hecho en cada etapa.
set -eu
cd "${0:A:h}"
[[ -d .venv ]] || { python3.13 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; }

temas=() audio=() solo_audio=0 sin_audio=0 corto=0
for a in "$@"; do
  case $a in
    --solo-audio) solo_audio=1 ;;
    --sin-audio) sin_audio=1 ;;
    --login|--dry-run) corto=1; audio+=($a) ;;
    <->) temas+=($a); audio+=($a) ;;
    *) audio+=($a) ;;
  esac
done

if (( ! sin_audio )); then
  .venv/bin/python pildoras_audio/pildoras.py "${audio[@]}"
fi
(( corto || solo_audio )) && exit 0

sel=(--all); (( $#temas )) && sel=(--pildora $temas)
.venv/bin/python 01_transcribir.py $sel --motor openrouter
.venv/bin/python 02_dosier.py $sel
.venv/bin/python 03_banco.py $sel
.venv/bin/python 04_examenes.py $sel
