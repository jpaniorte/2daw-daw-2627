# Generador de dosieres y controles de las píldoras

Convierte el audio de cada píldora de `digitalizacion/pildoras.md` en:

1. una **transcripción** (texto),
2. un **dosier** de estudio (Markdown),
3. un **banco de ~40 preguntas tipo test** validado por un segundo modelo,
4. **10 versiones de examen de 10 preguntas** (PDF imprimible + soluciones).

```
audio (Drive) ──01──▶ transcripción ──02──▶ dosier ──03──▶ banco de preguntas ──04──▶ 10 exámenes (PDF)
                     (Whisper)        (LLM)            (LLM + validador)          (sin IA, aleatorio)
```

Todo lo generado vive en `data/` y **no se sube a git ni a la web** (ver [Qué se sube y qué no](#qué-se-sube-y-qué-no)).

---

## 1. Requisitos e instalación (una sola vez)

| Qué | Para qué | Comprobar |
|---|---|---|
| Python **3.13** (o 3.12) | Intérprete. **No uses 3.14**: `faster-whisper` aún no tiene soporte | `python3.13 --version` |
| `ffmpeg` | Recomprime y trocea el audio | `ffmpeg -version` |
| `marp` (Marp CLI) | Genera el PDF de los exámenes (opcional: `--no-pdf` lo omite) | `marp --version` |
| Clave de OpenRouter | Transcripción, dosier y preguntas | <https://openrouter.ai/keys> |

```bash
cd digitalizacion/generador
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env        # y rellénalo (ver abajo)
```

`.env` (no se sube a git):

```
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=deepseek/deepseek-v4.1-flash          # generador de dosier y preguntas
OPENROUTER_VALIDATOR_MODEL=openai/gpt-6-luna           # validador (de OTRA familia que el generador)
OPENROUTER_STT_MODEL=openai/whisper-large-v3           # transcripción vía OpenRouter
```

> Si añades una línea al `.env` con `echo >>`, comprueba que el fichero termina en salto de línea; si no, la
> nueva se pega a la anterior y rompe las dos variables.

**Todos los comandos se ejecutan desde `digitalizacion/generador/` y con `.venv/bin/python`.**

---

## 2. Añadir una píldora nueva (receta completa)

### 2.1 Subir el audio y enlazarlo en `pildoras.md`

1. Sube el audio a la carpeta de Drive y compártelo como **«Cualquiera con el enlace»** (si es privado, la descarga falla).
2. Copia el enlace; el ID es lo que hay entre `/file/d/` y `/view`.
3. En `digitalizacion/pildoras.md`, en la fila de esa píldora, sustituye `Próximamente` y la celda vacía final:

```html
<tr>
<td>11</td><td>Título de la píldora</td><td class="pildora-reproductor"><a class="pildora-play-link" href="https://drive.google.com/file/d/ID_DEL_AUDIO/view" target="_blank" rel="noopener">&#9654; Reproducir audio</a></td><td class="pildora-completada"><button class="pildora-complete-btn" data-pildora="11" type="button">Marcar como completada</button></td>
</tr>
```

Los scripts **leen `pildoras.md`**: una píldora entra en el generador en cuanto tiene enlace de Drive. No hay otra lista que mantener.
Comprobación: `.venv/bin/python common.py --pildoras` (debe aparecer la nueva).

### 2.2 Generar todo

Atajo para el flujo entero (PDF en `pdf/N.pdf` → audio → Drive → web → transcripción → dosier → banco → exámenes):

```bash
./pildoras.sh 28          # o sin número: todas las pendientes
```

Ver `pildoras_audio/CLAUDE.md`. Paso a paso:

```bash
cd digitalizacion/generador
.venv/bin/python 01_transcribir.py --pildora 11 --motor openrouter
.venv/bin/python 02_dosier.py      --pildora 11
.venv/bin/python 03_banco.py       --pildora 11
.venv/bin/python 04_examenes.py    --pildora 11
```

Para **todas las que falten** (se saltan las ya hechas):

```bash
.venv/bin/python 01_transcribir.py --all --motor openrouter
.venv/bin/python 02_dosier.py --all
.venv/bin/python 03_banco.py --all
.venv/bin/python 04_examenes.py --all
```

### 2.3 Revisar antes de usar

- `data/dosieres/NN.md`: ¿recoge lo que dice el audio y no inventa nada?
- `data/bancos/NN.json`: lee unas 10 preguntas. Cada una lleva `cita` (frase del dosier que la justifica).
- `data/examenes/NN/pildora_NN_examen.pdf`: una página por versión.

---

## 3. Qué hace cada script

Todos aceptan `--pildora N [N ...]` o `--all`, y `--force` (rehacer aunque ya exista la salida).
**Son idempotentes**: sin `--force` se saltan lo que ya está hecho, así que si algo falla basta con relanzar.

### 01_transcribir.py — audio → texto

Descarga el audio de Drive (`gdown`) a `data/audio/NN/` y lo transcribe a `data/transcripciones/NN.txt`.

| Opción | Qué hace |
|---|---|
| `--motor openrouter` | **Recomendado.** Whisper vía API: ~1 min por audio y ~0,01-0,02 $. Recomprime a mono 48 kbps y trocea en bloques de 4 min (el proveedor corta a los 60 s por petición) |
| `--motor local` (por defecto) | `faster-whisper` en tu máquina. Gratis pero **muy lento en CPU** (más de 1 h para un audio de 18 min en un M1) |
| `--stt-model ID` | Modelo de transcripción de OpenRouter (def. `$OPENROUTER_STT_MODEL`) |
| `--trozo SEG` | Duración de cada trozo con `--motor openrouter` (def. 240) |
| `--whisper NOMBRE` | Modelo local: `small`, `medium`, `large-v3`, `large-v3-turbo`… |
| `--sufijo .xxx` | Guarda en `NN.xxx.txt` en vez de `NN.txt`; útil para **comparar motores** sin pisar nada |

Ver modelos de transcripción y su precio por hora de audio:

```bash
.venv/bin/python common.py --list-models --stt
.venv/bin/python common.py --list-models whisper --stt     # el filtro va justo detrás de --list-models
```

Limitaciones conocidas del modo OpenRouter: no se puede pasar glosario (el local sí), y la transcripción sale en un
bloque por trozo, sin saltos de párrafo dentro de cada uno.

### 02_dosier.py — texto → dosier

Usa `--model` (def. `$OPENROUTER_MODEL`). El prompt (`SYSTEM` en el propio script) obliga a:
usar **solo** lo que aparece en la transcripción, no añadir conocimiento externo, corregir términos mal oídos y
estructurar con títulos, listas, tablas, *Conceptos clave* y *Resumen*. Salida: `data/dosieres/NN.md`.

> Los audios son **diálogos entre dos presentadores**, no una clase; el prompt los convierte en apuntes.

### 03_banco.py — dosier → banco de preguntas

| Opción | Qué hace |
|---|---|
| `--model ID` | Generador (def. `$OPENROUTER_MODEL`) |
| `--validator-model ID` | Validador (def. `$OPENROUTER_VALIDATOR_MODEL`). Que sea de otra familia que el generador |
| `--preguntas N` | Preguntas a generar (def. 40) |
| `--seed N` | Semilla del reparto de letras (reproducible) |

Proceso: el generador crea N preguntas (4 opciones, 1 correcta, `cita`) → se descartan las defectuosas
(opciones repetidas, «todas las anteriores», «A y B»…) → se reparte la letra correcta de forma equilibrada
(A/B/C/D por igual) → el validador responde **a ciegas** usando el dosier → se marcan `validada: false` las que
discrepan. Salida: `data/bancos/NN.json`. Los prompts están en `SYSTEM_GEN` y `SYSTEM_VAL`.

### 04_examenes.py — banco → exámenes

No usa IA. Sin `--no-pdf` genera también el PDF con Marp.

| Opción | Qué hace |
|---|---|
| `--versiones N` | Número de versiones (def. 10) |
| `--preguntas N` | Preguntas por versión (def. 10) |
| `--seed N` | Semilla (reproducible) |
| `--no-pdf` | Solo el `.md` |
| `--rehacer` | Vuelve a montar el `.md`/`.pdf` desde `versiones.json`, **sin re-sortear** preguntas (las versiones y las claves no cambian) |
| `--claves` | Genera `data/examenes/claves.pdf` con las claves de todas las píldoras (varias por página) |

Cada versión elige preguntas **minimizando el solapamiento** con las anteriores (cada pregunta sale 2-3 veces en 10
versiones), baraja el orden y las opciones, y evita repartos con más de 3 respuestas de la misma letra.
Solo entran las preguntas con `validada` distinta de `false`; hacen falta al menos `--preguntas` válidas.

Salida en `data/examenes/NN/`:

| Fichero | Contenido |
|---|---|
| `pildora_NN_examen.pdf` / `.md` | Las 10 versiones, **una página A4 por versión**. Es un **cuadernillo reutilizable**: no lleva nombre ni fecha y se contesta en la hoja de respuestas |
| `pildora_NN_soluciones.md` | Tabla versión × pregunta con la letra correcta |
| `versiones.json` | Preguntas, orden y clave de cada versión (para trazabilidad o un corrector automático) |

Apto con **5 o más aciertos** sobre 10 (sin penalización por error), como dicen las normas de `pildoras.md`.

### 05_hoja_respuestas.py — hoja de respuestas del alumno

No usa IA ni datos generados: `python 05_hoja_respuestas.py` crea `hoja_respuestas.pdf` (se versiona, no contiene nada
secreto). Es **un folio A4 a doble cara**: un «Nombre y apellidos» por cara y **4 bloques por cara, 8 píldoras por folio**.
Cada bloque tiene **Píldora** (2 casillas), **Versión** (2 casillas), fecha, las 10 preguntas con casillas A-D y una
caja para el profesor (aciertos y APTO / NO APTO).

Uso en clase: se reparten los **cuadernillos** (los PDF de `04`, que se pueden reutilizar o proyectar) y cada alumno
contesta en su hoja, apuntando en un bloque nuevo la píldora y la versión que le han dado. Sin papel gastado por control.

### Corregir las hojas

- **Por lotes con escáner (recomendado):** `./corregir.sh`. Escanea a doble cara con el Brother ADS-2100e (reutiliza
  `~/workspace/autocorrector_test`, variable `AUTOCORRECTOR_DIR`), junta las soluciones de **todas las versiones de todas
  las píldoras** en `data/soluciones_pildoras.md`, lee con Claude cada control (admite **cuadernillos** con nombre y
  respuestas rodeadas y **hojas de respuestas**; ignora las caras en blanco y los bloques vacíos), decide APTO / NO APTO
  (5 o más de 10; si se repite una píldora cuenta el último intento) y regenera la página
  `digitalizacion/pildoras_resultados.md` (`/digitalizacion/pildoras/resultados/`): tabla con **Alumno** (iniciales,
  p. ej. J.A.E.), **Total** y **P1…P74** (`APTO`, `NO APTO` o `-`).

  | Opción | Qué hace |
  |---|---|
  | `--lote NOMBRE` | Nombre del lote (def. `pildoras_AAAAMMDD_HHMM`); si ya existe, se retoma |
  | `--sin-escanear [CARPETA]` | Sin escáner: importa PNG/JPG/PDF de CARPETA (o usa las páginas ya guardadas del lote) |
  | `--modelo sonnet` | Modelo de Claude para leer |
  | `--solo-publicar` | Solo regenera la página con los resultados guardados |
  | `--commit` | Hace commit de la página generada (el push lo haces tú) |

  Los datos (escaneos, lecturas, `data/resultados.json`) están en `data/`, no se suben; la página publicada solo lleva
  iniciales. Si una lectura sale con `¡Revisar!` (nombre dudoso, versión inexistente…), edita
  `data/corregir/LOTE/lecturas.json` y relanza con `--lote LOTE --sin-escanear`, conservando las lecturas.
  Pasos sueltos: `python corregir.py claves | leer LOTE | corregir LOTE | publicar | iniciales`.
- **A mano:** `data/examenes/claves.pdf` (`python 04_examenes.py --claves --all`) trae todas las claves; o la tabla de
  cada `pildora_NN_soluciones.md`.
- **Con fotos** (autocorrector, usa Claude Code con visión): deja las fotos de las caras en
  `autocorrector/sources/pildoras/` (no se suben a git) y ejecuta desde `autocorrector/`:

  ```bash
  ./get_results pildoras
  ```

  Devuelve una línea por bloque relleno: `Nombre · Píldora N · Versión V: A/10 aciertos → APTO|NO APTO · Errores: …`.
  Ignora los bloques vacíos, cuenta como fallo una pregunta sin marca o con dos, y añade `REVISAR A MANO` si la foto
  es dudosa. Es lectura por visión, no OCR determinista: revisa las fotos borrosas.

---

## 4. Estructura de carpetas

```
digitalizacion/generador/
├── LEEME.md              este fichero
├── common.py             parser de pildoras.md, cliente OpenRouter, listado de modelos
├── 01_transcribir.py     02_dosier.py     03_banco.py     04_examenes.py     05_hoja_respuestas.py
├── hoja_respuestas.pdf   hoja de respuestas (se versiona)
├── requirements.txt      .env.example     .env (local, ignorado)     .venv/ (ignorado)
└── data/                 (ignorado por git y por Jekyll)
    ├── audio/NN/             audio descargado
    ├── transcripciones/NN.txt
    ├── dosieres/NN.md
    ├── bancos/NN.json
    └── examenes/NN/          pildora_NN_examen.pdf|md, pildora_NN_soluciones.md, versiones.json
        claves.pdf              claves de todas las píldoras (--claves)
```

## 5. Qué se sube y qué no

- **Se versiona:** los scripts, `hoja_respuestas.pdf` (y su `.md`), `requirements.txt`, `.env.example` y este LEEME.
- **No se sube** (`.gitignore`): `data/`, `.env`, `.venv/`. Audios, transcripciones, dosieres, bancos y exámenes son
  material propio que no se publica.
- **Jekyll no publica nada de la carpeta** (`digitalizacion/generador` está en `exclude` de `_config.yml`).
- Los exámenes/solucionarios generados no deben acabar en el repo público; no muevas nada de `data/` fuera de esta carpeta.

---

## 6. Costes (referencia real)

Las 22 primeras píldoras costaron **≈1 $** en total, y casi todo fue un error evitable: DeepSeek v4.1 flash y
GPT-6 Luna son **modelos de razonamiento** y gastan tokens ocultos (que se cobran como salida) y a veces devuelven
«respuesta vacía», con reintentos que se cobran otra vez. Con el razonamiento apagado, un banco con validación
cuesta **~0,003 $** (frente a ~0,04 $ con él). Por eso `common.chat()` lo apaga por defecto
(`reasoning: {"enabled": false}`); pásale `razonar=True` solo si de verdad lo necesitas.
Si cambias a otro modelo, comprueba antes con una llamada mínima que `reasoning_tokens` sale a 0.

Reglas generales de coste:

- Transcripción por OpenRouter: ~0,01-0,02 $ por audio (el precio por hora varía según el proveedor al que enrute
  OpenRouter; se han visto 0,027-0,07 $/h).
- Dosier + banco + validación con los modelos de `.env`: menos de 1 céntimo por píldora.
- El script de transcripción imprime el coste real de cada audio. Para ver el gasto acumulado de la clave:
  OpenRouter → *Keys*, o `GET https://openrouter.ai/api/v1/key`.

Cambiar de modelo: `.venv/bin/python common.py --list-models [filtro]` muestra IDs y precio por millón de tokens.
Los modelos con sufijo (`:free`, `:batch`, `:thinking`) se comportan distinto; usa el ID sin sufijo salvo que sepas lo que haces.

---

## 7. Rehacer y ajustar

- Cambiar de modelo o de prompt y regenerar: usa `--force` **en ese paso y en los siguientes**. Cada paso lee la
  salida del anterior, así que si rehaces el dosier hay que rehacer también banco y exámenes (`--force` en 03 y 04).
- Regenerar el banco cambia los ids de pregunta: los exámenes antiguos dejan de corresponder a él.
- `04_examenes.py` con otra `--seed` (y `--force`) da otras 10 versiones sobre el mismo banco, sin gastar nada.

### Calidad conocida de las preguntas (píldora 1)

Observado al revisar el banco generado con DeepSeek v4.1 flash + validador GPT-6 Luna:

- **La opción correcta tiende a ser la más larga** (24 de 40 preguntas, frente al 25 % esperable al azar).
- **Distractores flojos** en algunas preguntas (opciones de otros temas del mismo dosier que se descartan a ojo).
- **Preguntas cortas, de memorizar definiciones.** Con «apto > 5/10» se aprueban con poca escucha.
- **El validador aceptó las 40**: tal como está no filtra casi nada.

Si quieres subir el nivel, ajusta los prompts de `03_banco.py`: pedir distractores del mismo tema, preguntas de
aplicación («¿qué pasa si…?») y exigir que la correcta no sea la más larga; y hacer el validador más estricto
(que señale preguntas ambiguas o con distractores absurdos). También puedes probar un generador más potente.

---

## 8. Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `TypeError: open() got an unexpected keyword argument 'metadata_errors'` | `faster-whisper` y PyAV incompatibles. Ya está fijado `av<17` en `requirements.txt`; reinstala con `.venv/bin/pip install -r requirements.txt` |
| `faster-whisper` no instala | Estás con Python 3.14. Crea el venv con `python3.13` |
| `No se pudo descargar la píldora N` | El audio de Drive no es público («Cualquiera con el enlace») o el ID del enlace es incorrecto |
| `Sin audio en pildoras.md` | La fila no tiene enlace `/file/d/ID` en la celda del reproductor; revisa el formato de la sección 2.1 |
| `Falta OPENROUTER_API_KEY` | El `.env` no existe, está vacío o no está guardado. Comprueba que estás en `digitalizacion/generador/` |
| HTTP 401/402 de OpenRouter | Clave inválida o sin crédito/límite. Mira *Keys* en OpenRouter |
| HTTP 429/5xx | Se reintenta solo 3 veces; si persiste, relanza más tarde (el script retoma donde se quedó) |
| La transcripción local no avanza | Es normal en CPU (muy lenta). Usa `--motor openrouter` o `--whisper large-v3-turbo` |
| El PDF sale con el contenido en medio de la página | Es el tema `a4-print` de Marp (centra en vertical); ya se fuerza `place-content: flex-start` en `04_examenes.py` |
| `marp` tarda mucho la primera vez | Arranca Chrome; después es rápido. `--no-pdf` lo salta |
| `python: can't open file 'common.py'` | Estás en otra carpeta. Entra en `digitalizacion/generador/` y usa `.venv/bin/python` |
| El gasto sube mucho / «respuesta vacía» en los reintentos | Modelo de razonamiento con el razonamiento activo. Ver sección 6. Para y revisa el gasto antes de relanzar |
| `El banco solo tiene N preguntas válidas` | El validador descartó demasiadas. Regenera con `--preguntas 50 --force` o cambia de modelo |

---

## 9. Automatización del audio (`pildoras_audio/`)

Contexto para continuar el trabajo (antes en `pildoras_audio/CLAUDE.md`). Automatiza: PDF del tema N → podcast en Gemini Notebook → m4a → mp3 → Google Drive → fila N de la web; después `pildoras.sh` encadena los pasos 01–04. El usuario es profesor de ciclo formativo (oposición de informática, 74 temas). Idioma de trabajo: español.

### Rutas clave
- Esta carpeta: código del flujo. `generador/pdf/N.pdf` entrada (N = número de tema INF, 1–74).
- `/Users/jose/workspace/audio_seat/`: `convert.sh` (m4a→mp3, idempotente, no modificar), `Pildora_N__Titulo.m4a`, `mp3/NN - Titulo.mp3`. Ver su `CLAUDE.md`. Los m4a pesan decenas de MB: no leerlos.
- `/Users/jose/workspace/DAW/digitalizacion/pildoras.md`: tabla HTML de la web (repo git `jpaniorte/2daw-daw-2627`, rama `main`, GitHub Pages: https://jpaniorte.github.io/2daw-daw-2627/digitalizacion/pildoras/). Fuente de los títulos oficiales por número. El repo tiene otros cambios sin commitear del usuario: al publicar, `git add` solo `digitalizacion/pildoras.md`.
- Carpeta de Drive de destino: ID `14KQ3cH_6KbgembIoxINqVeQRMoBPd80m` (en `pildoras_audio/config.env`).

### Uso
`./pildoras.sh [N ...] [--max K] [--dry-run] [--login] [--commit] [--solo-audio] [--sin-audio]` (ver 2.2). La etapa de audio es `pildoras_audio/pildoras.py`.
Idempotente: salta lo hecho según `state.json` (por tema: `m4a, mp3, drive_id, web`) y el enlace ya presente en `pildoras.md`. Un tema con m4a local reutiliza el audio aunque no haya PDF. Falla por tema sin parar el lote.
Módulos: `pildoras.py` (orquestador), `notebooklm.py`, `drive_upload.py`, `update_md.py`, `common.py`.

### Credenciales y cuentas (no volcar secretos en chat ni en el repo)
- Cuenta de trabajo en Google: la cuenta personal de José que tiene el proyecto de Cloud, Drive y Gemini Notebook (el e-mail no se escribe aquí porque este fichero se versiona en un repo público). No asumir otra.
- OAuth de escritorio: `~/.pildoras/client_secret.json` (fuera del proyecto) y token `~/.pildoras/drive_token.json`. Proyecto de Cloud en modo Pruebas con esa cuenta como tester; scope `drive.file`. Los mp3 se suben y se comparten "cualquiera con el enlace: lector". La Drive API es gratuita.
- Sesión de Gemini Notebook: Chrome real con perfil propio `~/.pildoras/chrome-real` y depuración remota (puerto 9222). El Chromium de Playwright es rechazado por Google ("navegador no seguro"), por eso se usa Chrome + `connect_over_cdp`. Login ya hecho y verificado.

### Estado (2026-11-03)
- En la web hay **28 píldoras** con audio: 1–10, 13, 15, 21, 23, 25, 26, 27, 30, 32, 33, 34, 35, 38, 40, 46, 48, 68, 74. Publicado en el commit `0c699eb` (25, 26, 32, 33, 35 y 38 las subió este flujo).
- Con PDF pero **sin audio**: 24, 28, 29, 31, 39. El audio de la 39 se borró a propósito (era de vídeo digital, no de SQL).
- Faltan PDFs: 11, 12, 14, 16–20, 22, 36, 37, 41–45, 47, 49–67, 69–73.
- Duplicados `1_resumen.pdf` y `2_resumen.pdf` (ignorados). Los PDF `27, 30, 40, 48` son resúmenes cortos, el resto son el tema completo (`...TL`).
- **Tema 24 hecho (3 nov):** audio generado a mano con el script de exploración en el cuaderno `https://notebook.google.com/notebook/ee0dcc55-5a16-430d-84b2-b8258175d757` (23 min; las 28 actuales duran de media 19,8 min, de 11 a 28), descargado, convertido, subido a Drive y enlazado en `pildoras.md` **en local; falta commit + push** (esperar a que el usuario lo pida).
- Con PDF y sin audio quedan: 28, 29, 31, 39. Siguiente paso: probar `./pildoras.sh 28` para validar el `generate_audio` nuevo **de punta a punta** (aún sin probar; consume una generación diaria y tarda ~8 min).

### Gemini Notebook: lo ya descubierto (https://notebook.google.com/, UI en español)
- Home: botón "Nuevo cuaderno" → navega a `/notebook/<id>`.
- Subir fuente: botón `Añadir fuente` → `Subir archivos` abre un file chooser (`page.expect_file_chooser`); la fuente aparece como `N.pdf`.
- Audio: tarjeta "Resumen de audio" (Studio) → diálogo `mat-dialog-container` "Personalizar resumen de audio" (formato, idioma español por defecto, duración Corto/Predeterminada, `textarea` del prompt) → botón "Generar ahora".
- La página no llega nunca a `networkidle`: usar `wait_until="domcontentloaded"` y esperar a elementos.
- Fin de la generación: en el panel Studio aparece un elemento con botón `Reproducir` (tarda ~7-8 min). Descarga: botón `Más` (el último de la página; el primero es el de la fuente) → `menuitem` "Descargar" → m4a (nombre sugerido = título que pone Google, p. ej. `Anatomía_y_modelos_de_ejecución_del_código.m4a`).
- `notebooklm.py` ya implementa todo el flujo con esos localizadores (`generate_audio(n, pdf, audio_dir)` devuelve `audio_seat/Pildora_N__<titulo de Google>.m4a`) y lanza Chrome en headless por CDP. Está escrito pero **sin probar entero**; solo se validaron a mano los pasos sueltos.
- Cada ejecución crea un cuaderno nuevo en la cuenta del usuario (quedan en su lista; no los borramos).
- Scripts de exploración en el scratchpad de la sesión, no en el repo. Para explorar sin ventana: Chrome `--headless=new --remote-debugging-port=9223 --user-data-dir=~/.pildoras/chrome-real`. Cerrar antes cualquier Chrome que use ese perfil.

### Prompt de NotebookLM (constante `PROMPT` en `notebooklm.py`)
Profesor de CFGS, serie "píldoras", ameno, 10–15 min, ejemplos fáciles, basado en `{N}.pdf`.

### Cosas a recordar
- **Repo público (GitHub Pages).** Los PDF de `pdf/` son de una academia externa con derechos de terceros: están en el `.gitignore` de DAW (como `pildoras.pdf`) y la carpeta entera está en `exclude` de `_config.yml`. No quitar esas reglas ni hacer `git add -f`. Al publicar, `git add` solo `digitalizacion/pildoras.md` (y esta carpeta, si el usuario quiere versionar el código, sin `pdf/`, `.venv/`, `logs/`).
- Las pruebas reales crean cuadernos y consumen audios diarios del usuario; no borrar sus cuadernos sin permiso.
- Publicar la web = commit + push a `main` de DAW; solo cuando el usuario lo pide.
- Alternativas si Gemini Notebook por navegador resulta frágil: ElevenLabs (~100 $ el lote) o LLM + OpenAI TTS (~5–10 €); el resto del flujo no cambia.
- Si el nombre del m4a no sigue `Pildora_N_Titulo.m4a`, `convert.sh` lo ignora con un aviso.
