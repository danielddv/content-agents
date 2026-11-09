"""Herramientas de vídeo (FFmpeg, gratis y en local).

Uso:
    python -m tools.video info VIDEO
    python -m tools.video cortar VIDEO --inicio 12.5 --fin 48 --out clip.mp4
    python -m tools.video quitar-silencios VIDEO --out limpio.mp4 [--umbral -35] [--minimo 0.6]
    python -m tools.video vertical VIDEO --marca personal --out final.mp4 [--subs subs.ass]
    python -m tools.video clip VIDEO --inicio 12.5 --fin 48 --marca personal --out-dir carpeta/
        (todo en uno: cortar → quitar silencios → transcribir → vertical con subtítulos)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from core.brand import brand_settings
from tools.subtitles import write_ass

ENCODE = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
          "-movflags", "+faststart"]


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"Error de FFmpeg:\n{result.stderr[-2000:]}")
    return result.stderr


def info(video: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
                          "-of", "json", str(video)], capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    v = next((s for s in data["streams"] if s["codec_type"] == "video"), {})
    return {"duracion": float(data["format"]["duration"]), "ancho": v.get("width"), "alto": v.get("height"),
            "audio": any(s["codec_type"] == "audio" for s in data["streams"])}


def cut(video: Path, start: float, end: float, out: Path) -> Path:
    run(["ffmpeg", "-y", "-ss", str(start), "-to", str(end), "-i", str(video), *ENCODE, str(out)])
    return out


def silences(video: Path, threshold_db: float = -35, min_len: float = 0.6) -> list[tuple[float, float]]:
    log = run(["ffmpeg", "-i", str(video), "-af", f"silencedetect=noise={threshold_db}dB:d={min_len}",
               "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    if len(ends) < len(starts):
        ends.append(info(video)["duracion"])
    return list(zip(starts, ends))


def remove_silences(video: Path, out: Path, threshold_db: float = -35, min_len: float = 0.6,
                    keep: float = 0.15) -> Path:
    """Quita las pausas largas, dejando un pequeño margen para que el corte suene natural."""
    duration = info(video)["duracion"]
    gaps = silences(video, threshold_db, min_len)
    if not gaps:
        shutil.copy(video, out)
        return out
    keep_ranges, cursor = [], 0.0
    for s, e in gaps:
        if s + keep > cursor:
            keep_ranges.append((cursor, s + keep))
        cursor = max(cursor, e - keep)
    if cursor < duration:
        keep_ranges.append((cursor, duration))
    expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep_ranges)
    run(["ffmpeg", "-y", "-i", str(video),
         "-vf", f"select='{expr}',setpts=N/FRAME_RATE/TB",
         "-af", f"aselect='{expr}',asetpts=N/SR/TB", *ENCODE, str(out)])
    return out


def _ass_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def vertical(video: Path, out: Path, style: dict[str, str], subs: Path | None = None) -> Path:
    """Pasa a 1080x1920 (9:16) y, si se indica, incrusta los subtítulos."""
    sub_filter = f",ass='{_ass_path(subs)}'" if subs else ""
    if style.get("encuadre") == "relleno":
        vf = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];"
              "[b]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1{sub_filter}")
    else:
        vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1{sub_filter}"
    run(["ffmpeg", "-y", "-i", str(video), "-filter_complex", vf, "-r", "30", *ENCODE, str(out)])
    return out


def make_clip(video: Path, start: float | None, end: float | None, brand: str, out_dir: Path,
              name: str = "clip", model: str = "small") -> dict:
    from tools.transcribe import transcribe

    style = brand_settings(brand)
    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / f"{name}_trabajo"
    work.mkdir(exist_ok=True)

    current = video
    if start is not None and end is not None:
        current = cut(video, start, end, work / "1_corte.mp4")
    if style.get("quitar_silencios", "si").lower() in ("si", "sí", "yes", "true"):
        current = remove_silences(current, work / "2_sin_silencios.mp4")
    transcript_path = work / "transcripcion.json"
    transcribe(current, transcript_path, model)
    subs = write_ass(transcript_path, style, work / "subtitulos.ass")
    final = vertical(current, out_dir / f"{name}.mp4", style, subs)
    return {"video": str(final), "transcripcion": str(transcript_path.with_suffix(".txt")),
            "duracion": round(info(final)["duracion"], 1)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("info"); s.add_argument("video", type=Path)
    s = sub.add_parser("cortar"); s.add_argument("video", type=Path)
    s.add_argument("--inicio", type=float, required=True); s.add_argument("--fin", type=float, required=True)
    s.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("quitar-silencios"); s.add_argument("video", type=Path)
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("--umbral", type=float, default=-35); s.add_argument("--minimo", type=float, default=0.6)
    s = sub.add_parser("vertical"); s.add_argument("video", type=Path)
    s.add_argument("--marca", required=True); s.add_argument("--out", type=Path, required=True)
    s.add_argument("--subs", type=Path)
    s = sub.add_parser("clip"); s.add_argument("video", type=Path)
    s.add_argument("--inicio", type=float); s.add_argument("--fin", type=float)
    s.add_argument("--marca", required=True); s.add_argument("--out-dir", type=Path, required=True)
    s.add_argument("--nombre", default="clip"); s.add_argument("--modelo", default="small")

    a = p.parse_args()
    if a.cmd == "info":
        print(json.dumps(info(a.video), ensure_ascii=False))
    elif a.cmd == "cortar":
        print(cut(a.video, a.inicio, a.fin, a.out))
    elif a.cmd == "quitar-silencios":
        print(remove_silences(a.video, a.out, a.umbral, a.minimo))
    elif a.cmd == "vertical":
        print(vertical(a.video, a.out, brand_settings(a.marca), a.subs))
    elif a.cmd == "clip":
        print(json.dumps(make_clip(a.video, a.inicio, a.fin, a.marca, a.out_dir, a.nombre, a.modelo),
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
