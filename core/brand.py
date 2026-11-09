"""Lee los perfiles de marca (brands/*.md y brands/flying-frames/*.md)."""

from __future__ import annotations

import re
from pathlib import Path

BRANDS_DIR = Path(__file__).resolve().parent.parent / "brands"

DEFAULTS = {
    "subtitulos": "palabra",
    "color_texto": "#FFFFFF",
    "color_resaltado": "#FFD400",
    "fuente": "DejaVu Sans",
    "encuadre": "recorte",
    "quitar_silencios": "si",
}


def find_brand(name: str) -> Path:
    for path in sorted(BRANDS_DIR.rglob("*.md")):
        if path.stem == name and not path.stem.startswith("_") and path.stem != "README":
            return path
    available = sorted(p.stem for p in BRANDS_DIR.rglob("*.md")
                       if not p.stem.startswith("_") and p.stem != "README")
    raise SystemExit(f"No existe la marca '{name}'. Marcas disponibles: {', '.join(available)}")


def brand_settings(name: str) -> dict[str, str]:
    """Ajustes de vídeo de la cabecera (entre las líneas ---) del perfil de marca."""
    settings = dict(DEFAULTS)
    lines = find_brand(name).read_text(encoding="utf-8").splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" in line:
                key, value = line.split(":", 1)
                value = value.strip()
                quoted = re.match(r'"([^"]*)"', value)
                value = quoted.group(1) if quoted else value.split(" #", 1)[0].strip()
                settings[key.strip()] = value
    return settings
