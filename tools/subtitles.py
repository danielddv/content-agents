"""Genera subtítulos .ass (estilo de la marca) a partir de una transcripción."""

from __future__ import annotations

import json
from pathlib import Path

W, H = 1080, 1920


def _ass_color(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}".upper()


def _ts(t: float) -> str:
    t = max(t, 0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _esc(text: str) -> str:
    return text.replace("\\", "").replace("{", "(").replace("}", ")")


def build_ass(transcript: dict, style: dict[str, str]) -> str:
    words = [w for s in transcript["segments"] for w in s.get("words", []) if w["word"]]
    mode = style.get("subtitulos", "palabra")
    text_c = _ass_color(style.get("color_texto", "#FFFFFF"))
    hi_c = _ass_color(style.get("color_resaltado", "#FFD400"))
    font = style.get("fuente", "DejaVu Sans")

    if mode == "clasico":
        size, align, margin_v, outline = 58, 2, 220, 3
    else:
        size, align, margin_v, outline = 92, 5, 0, 6

    header = (
        "[Script Info]\nScriptType: v4.00+\n"
        f"PlayResX: {W}\nPlayResY: {H}\nWrapStyle: 0\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Main,{font},{size},{text_c},{text_c},&H00000000,&H80000000,"
        f"-1,0,0,0,100,100,0,0,1,{outline},2,{align},80,80,{margin_v},1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    events: list[str] = []

    if mode == "clasico":
        line: list[dict] = []
        for i, w in enumerate(words):
            line.append(w)
            text = " ".join(x["word"] for x in line)
            last = i == len(words) - 1
            gap = not last and words[i + 1]["start"] - w["end"] > 0.6
            if len(text) > 32 or w["word"][-1:] in ".?!" or gap or last:
                events.append(f"Dialogue: 0,{_ts(line[0]['start'])},{_ts(w['end'])},Main,,0,0,0,,{_esc(text)}")
                line = []
    else:
        # Grupos de hasta 3 palabras; la palabra que se está diciendo va resaltada.
        groups: list[list[dict]] = []
        for w in words:
            if not groups or len(groups[-1]) >= 3 or w["start"] - groups[-1][-1]["end"] > 0.5 \
                    or groups[-1][-1]["word"][-1:] in ".?!,":
                groups.append([])
            groups[-1].append(w)
        for g in groups:
            for j, w in enumerate(g):
                end = g[j + 1]["start"] if j + 1 < len(g) else w["end"]
                parts = [
                    (f"{{\\c{hi_c}}}{_esc(x['word']).upper()}{{\\c{text_c}}}" if k == j else _esc(x["word"]).upper())
                    for k, x in enumerate(g)
                ]
                events.append(f"Dialogue: 0,{_ts(w['start'])},{_ts(end)},Main,,0,0,0,,{' '.join(parts)}")

    return header + "\n".join(events) + "\n"


def write_ass(transcript_path: Path, style: dict[str, str], out: Path) -> Path:
    transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
    out.write_text(build_ass(transcript, style), encoding="utf-8")
    return out
