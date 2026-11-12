import re
from pathlib import Path


def update_md(md_path, n, file_id):
    p = Path(md_path)
    text = p.read_text()
    pattern = re.compile(
        rf'(<td>{n}</td><td>.*?</td>)<td class="pildora-reproductor">Próximamente</td>'
        r'<td class="pildora-completada"></td>'
    )
    if not pattern.search(text):
        raise RuntimeError(f"Fila {n} no encontrada o ya tiene enlace en {md_path}")
    link = (
        '<td class="pildora-reproductor"><a class="pildora-play-link" '
        f'href="https://drive.google.com/file/d/{file_id}/view" target="_blank" rel="noopener">'
        '&#9654; Reproducir audio</a></td>'
        f'<td class="pildora-completada"><button class="pildora-complete-btn" data-pildora="{n}" '
        'type="button">Marcar como completada</button></td>'
    )
    p.write_text(pattern.sub(lambda m: m.group(1) + link, text, count=1))
