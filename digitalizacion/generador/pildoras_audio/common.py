import json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = HERE / "state.json"
HOME_DIR = Path.home() / ".pildoras"


def load_config():
    cfg = {}
    for line in (HERE / "config.env").read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            cfg[k.strip()] = os.path.expanduser(v.strip())
    return cfg


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def md_titles(md_path):
    """{n: titulo} a partir de las filas de la tabla de pildoras.md."""
    text = Path(md_path).read_text()
    rows = re.findall(r"<td>(\d+)</td><td>(.*?)</td><td class=\"pildora-reproductor\">", text)
    return {int(n): t for n, t in rows}


def md_has_link(md_path, n):
    text = Path(md_path).read_text()
    m = re.search(rf"<td>{n}</td><td>.*?</td><td class=\"pildora-reproductor\">(.*?)</td>", text)
    return bool(m and "pildora-play-link" in m.group(1))
