#!/bin/zsh
# Corrige los controles de las píldoras escaneados y publica la tabla de resultados.
#   escanear (doble cara) -> soluciones de todas las versiones -> lectura con Claude -> APTO/NO APTO
#   -> digitalizacion/pildoras_resultados.md  (/digitalizacion/pildoras/resultados/)
#
# Entran cuadernillos (nombre manuscrito y respuestas rodeadas) y hojas de respuestas (hoja_respuestas.pdf).
# APTO con 5 o más aciertos de 10. Si un alumno repite una píldora, cuenta el último intento.
#
# Uso: ./corregir.sh [--lote NOMBRE] [--sin-escanear [CARPETA]] [--modelo sonnet] [--solo-publicar] [--commit]
#   --lote NOMBRE            nombre del lote (def. pildoras_AAAAMMDD_HHMM); si ya existe, se retoma
#   --sin-escanear [CARPETA] no usa el escáner: importa las imágenes/PDF de CARPETA al lote
#                            (sin CARPETA, usa las páginas que ya hay en data/corregir/LOTE)
#   --solo-publicar          solo regenera la página con los resultados guardados
#   --commit                 commit de la página generada (el push lo haces tú)
# Variables: AUTOCORRECTOR_DIR (def. ~/workspace/autocorrector_test, con escanear.py, ia.py y alumnos_daw.txt)
set -eu
cd "${0:A:h}"
[[ -d .venv ]] || { python3.13 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; }
.venv/bin/python -c "import PIL" 2>/dev/null || .venv/bin/pip install -q pillow

AUTO=${AUTOCORRECTOR_DIR:-$HOME/workspace/autocorrector_test}
export AUTOCORRECTOR_DIR=$AUTO
DATA=${CORREGIR_DATA:-data}
lote="pildoras_$(date +%Y%m%d_%H%M)" carpeta="" escanear=1 modelo=sonnet solo_publicar=0 commit=0
while (( $# )); do
  case $1 in
    --lote) lote=$2; shift ;;
    --modelo) modelo=$2; shift ;;
    --sin-escanear) escanear=0; if [[ ${2:-} != "" && ${2:-} != --* ]]; then carpeta=$2; shift; fi ;;
    --solo-publicar) solo_publicar=1 ;;
    --commit) commit=1 ;;
    -h|--help) sed -n '2,15p' $0; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 1 ;;
  esac
  shift
done

py=.venv/bin/python
destino=$DATA/corregir/$lote

publicar() {
  $py corregir.py publicar
  if (( commit )); then
    pagina=${CORREGIR_PAGINA:-../pildoras_resultados.md}
    git add "$pagina"
    git diff --cached --quiet -- "$pagina" || git commit -q -m "Resultados de los controles de las píldoras ($lote)" -- "$pagina"
    echo "Commit hecho; falta el push."
  fi
}

(( solo_publicar )) && { publicar; exit 0 }

[[ -d $AUTO/examenes ]] || { echo "No encuentro $AUTO/examenes (define AUTOCORRECTOR_DIR)" >&2; exit 1 }

si() { local r; print -n "$1 [s/n] "; read -u 0 -k 1 r; echo; [[ $r == [sSyY] ]] }
paginas() { local f; f=($destino/pag_*.png(N)); echo $#f }

# 1. Escanear (por tandas) o importar
mkdir -p $destino
if (( escanear )); then
  set +e
  (cd $AUTO/examenes && $AUTO/.venv/bin/python escanear.py --lote $lote --continuar)
  rc=$?
  set -e
  # las hojas completas se guardan aunque haya habido atasco
  cp $AUTO/examenes/escaneos/$lote/pag_*.png $destino/ 2>/dev/null || true
  case $rc in
    0) ;;
    2) echo "Atasco o error: saca las hojas atascadas (apaga y enciende el escáner si el ! parpadea), cárgalas y relanza con --lote $lote" >&2; exit 2 ;;
    3) echo "El escáner no detecta hojas: cárgalas (hasta el tope) y vuelve a lanzar." >&2; exit 3 ;;
    *) echo "Ha fallado el escaneo." >&2; exit 1 ;;
  esac
elif [[ -n $carpeta ]]; then
  n=$(paginas)
  for f in $carpeta/*(.N); do
    case ${f:l} in
      *.pdf) tmp=$(mktemp -d); pdftoppm -r 200 -png $f $tmp/p
             for p in $tmp/p*.png; do n=$((n+1)); cp $p $destino/pag_$(printf %03d $n).png; done; rm -rf $tmp ;;
      *.png|*.jpg|*.jpeg) n=$((n+1)); $py -c "import sys; from PIL import Image; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2])" $f $destino/pag_$(printf %03d $n).png ;;
    esac
  done
fi
(( $(paginas) )) || { echo "No hay páginas en $destino" >&2; exit 1 }
echo "$(paginas) páginas en $destino"

# 2. Soluciones de todas las versiones de todas las píldoras
$py corregir.py claves

# 3. Leer con Claude
conservar=0
if [[ -f $destino/lecturas.json ]]; then
  si "Ya hay lecturas de este lote. ¿Las conservo (p. ej., porque las has corregido a mano)?" && conservar=1
  echo
fi
if (( ! conservar )); then
  set +e; $py corregir.py leer $lote --modelo $modelo; rc=$?; set -e
  if (( rc != 0 )); then
    echo "\nRevisa $destino/lecturas.json y relanza: ./corregir.sh --lote $lote --sin-escanear" >&2
    exit $rc
  fi
fi

# 4. Corregir y publicar
echo
$py corregir.py corregir $lote
publicar
