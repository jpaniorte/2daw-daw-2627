#!/usr/bin/env python3
"""Orquestador: PDF -> NotebookLM -> mp3 -> Drive -> pildoras.md (idempotente)."""
import argparse
import re
import subprocess
import sys
import traceback
from pathlib import Path

from common import load_config, load_state, md_has_link, save_state

STAGES = ["m4a", "mp3", "drive_id", "web"]


def pending(cfg, state, only):
    pdfs = {int(p.stem): p for p in Path(cfg["PDF_DIR"]).glob("*.pdf") if p.stem.isdigit()}
    # Temas con audio ya generado en audio_seat aunque no tengan PDF aquí
    local = {int(m.group(1)) for f in Path(cfg["AUDIO_DIR"]).glob("Pildora_*.m4a")
             if (m := re.match(r"Pildora_(\d+)_", f.name))}
    todo = []
    for n in sorted(set(pdfs) | local):
        if only and n not in only:
            continue
        if md_has_link(cfg["PILDORAS_MD"], n) or state.get(str(n), {}).get("web"):
            continue
        todo.append((n, pdfs.get(n)))
    return todo


def process(n, pdf, cfg, state):
    from drive_upload import upload_mp3
    from notebooklm import generate_audio
    from update_md import update_md

    st = state.setdefault(str(n), {})
    audio_dir = Path(cfg["AUDIO_DIR"])

    existing = next(iter(sorted(audio_dir.glob(f"Pildora_{n}_*.m4a"))), None)
    if existing:
        st["m4a"] = str(existing)
    else:
        if pdf is None:
            raise RuntimeError(f"Sin PDF ni m4a para la píldora {n}")
        st["m4a"] = str(generate_audio(n, pdf, audio_dir))
    save_state(state)

    mp3 = next(iter(sorted((audio_dir / "mp3").glob(f"{n:02d} - *.mp3"))), None)
    if not (st.get("mp3") and mp3):
        subprocess.run([str(audio_dir / "convert.sh")], check=True)
        mp3 = next(iter(sorted((audio_dir / "mp3").glob(f"{n:02d} - *.mp3"))), None)
        if not mp3:
            raise RuntimeError(f"convert.sh no generó el mp3 de la píldora {n}")
        st["mp3"] = str(mp3); save_state(state)

    if not st.get("drive_id"):
        st["drive_id"] = upload_mp3(mp3, cfg["DRIVE_FOLDER_ID"], cfg["DRIVE_CLIENT_SECRET"])
        save_state(state)

    update_md(cfg["PILDORAS_MD"], n, st["drive_id"])
    st["web"] = True; save_state(state)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("temas", nargs="*", type=int)
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--login", action="store_true", help="iniciar sesión en NotebookLM")
    ap.add_argument("--commit", action="store_true", help="git commit de pildoras.md al terminar")
    a = ap.parse_args()

    if a.login:
        from notebooklm import login
        return login()

    cfg, state = load_config(), load_state()
    todo = pending(cfg, state, set(a.temas))
    if a.max:
        todo = todo[: a.max]
    print(f"Pendientes: {[n for n, _ in todo] or 'ninguna'}")
    if a.dry_run or not todo:
        return
    if not cfg.get("DRIVE_FOLDER_ID"):
        sys.exit("Falta DRIVE_FOLDER_ID en config.env")

    done, failed = [], []
    for n, pdf in todo:
        print(f"== Píldora {n}")
        try:
            process(n, pdf, cfg, state)
            done.append(n)
        except Exception:
            traceback.print_exc()
            failed.append(n)
    print(f"Hechas: {done}  Fallidas: {failed}")
    if failed:
        sys.exit(1)

    if a.commit and done:
        md = Path(cfg["PILDORAS_MD"])
        subprocess.run(["git", "-C", str(md.parent), "add", md.name], check=True)
        subprocess.run(["git", "-C", str(md.parent), "commit", "-m",
                        f"Añade audio de las píldoras {', '.join(map(str, done))}"], check=True)


if __name__ == "__main__":
    main()
