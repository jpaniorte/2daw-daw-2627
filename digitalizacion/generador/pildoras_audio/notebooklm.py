"""Automatiza NotebookLM (Gemini Notebook) con tu Chrome real y un perfil propio.

Google bloquea el inicio de sesión en el Chromium de Playwright, así que se lanza
Chrome normal con depuración remota y el script se conecta por CDP.

Si Google cambia la interfaz, hay que recalibrar los localizadores de generate_audio
(se guardan capturas en logs/ cuando algo falla).
"""
import re
import socket
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from common import HERE, HOME_DIR

PROFILE = HOME_DIR / "chrome-real"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CDP_PORT = 9222
URL = "https://notebook.google.com/"
GENERATION_TIMEOUT_S = 25 * 60

PROMPT = (
    "Soy un profesor de ciclo formativo de grado superior que quiero realizar una serie de "
    "podcast sobre temas de informatica. Lo llamo pildoras. Van dirigidas a estudiantes de "
    "ciclo formativo de grado superior. Debe ser ameno y entretenido, la finalidad es que "
    "disfruten y despertar su curiosidad sobre temas interesantes, por lo que no deben ser "
    "muy extensos 10-15min. Con ejemplos faciles de entender. Básate en el documento {n}.pdf"
)

def _shot(page, name):
    (HERE / "logs").mkdir(exist_ok=True)
    page.screenshot(path=str(HERE / "logs" / f"{name}-{int(time.time())}.png"))


def _chrome(headless=False):
    """Arranca Chrome con el perfil propio si no está ya escuchando en CDP_PORT."""
    def up():
        with socket.socket() as c:
            c.settimeout(0.3)
            return c.connect_ex(("127.0.0.1", CDP_PORT)) == 0
    if up():
        return None
    PROFILE.mkdir(parents=True, exist_ok=True)
    args = [CHROME, f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={PROFILE}", "--no-first-run"]
    if headless:
        args.append("--headless=new")
    proc = subprocess.Popen(args + [URL])
    for _ in range(60):
        if up():
            return proc
        time.sleep(0.5)
    raise RuntimeError("Chrome no abrió el puerto de depuración")


def login():
    """Abre el navegador para iniciar sesión manualmente una sola vez."""
    proc = _chrome()
    print("Inicia sesión en Gemini Notebook y cierra Chrome (Cmd+Q) para guardar la sesión.")
    if proc:
        proc.wait()


def generate_audio(n, pdf_path, audio_dir):
    """Crea un cuaderno con el PDF, genera el resumen de audio y lo descarga.

    Devuelve la ruta del m4a: audio_dir/Pildora_N__<titulo que da Google>.m4a
    """
    HOME_DIR.mkdir(exist_ok=True)
    proc = _chrome(headless=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
            page = browser.contexts[0].new_page()
            page.set_viewport_size({"width": 1400, "height": 1000})
            try:
                # La página nunca queda "idle" por red: se espera a elementos concretos
                page.goto(URL, wait_until="domcontentloaded", timeout=60_000)
                page.get_by_role("button", name="Nuevo cuaderno").click(timeout=60_000)
                page.wait_for_url(re.compile(r"/notebook/"), timeout=60_000)

                page.get_by_role("button", name="Añadir fuente").first.click(timeout=60_000)
                with page.expect_file_chooser() as fc:
                    page.get_by_text("Subir archivos").first.click()
                fc.value.set_files(str(pdf_path))
                page.get_by_role("button", name=Path(pdf_path).name).wait_for(timeout=120_000)

                # Mientras Notebook procesa la fuente el clic se pierde: reintentar hasta que abra el diálogo
                dialog = page.locator("mat-dialog-container")
                for _ in range(20):
                    page.get_by_text("Resumen de audio").first.click()
                    try:
                        dialog.locator("textarea").first.wait_for(timeout=8_000)
                        break
                    except Exception:
                        time.sleep(3)
                dialog.locator("textarea").first.fill(PROMPT.format(n=n))
                dialog.get_by_role("button", name="Generar ahora").click()

                # Cuando termina, el elemento del panel Studio muestra el botón Reproducir
                page.get_by_role("button", name="Reproducir").first.wait_for(
                    timeout=GENERATION_TIMEOUT_S * 1000)

                # El botón "Más" del audio es el último (el primero es el de la fuente)
                page.get_by_role("button", name="Más").last.click()
                with page.expect_download(timeout=300_000) as dl:
                    page.get_by_role("menuitem", name="Descargar").click()
                out = Path(audio_dir) / f"Pildora_{n}__{dl.value.suggested_filename}"
                dl.value.save_as(str(out))
                return out
            except Exception:
                _shot(page, f"fallo-{n}")
                raise
            finally:
                page.close()
    finally:
        if proc:
            proc.terminate()
