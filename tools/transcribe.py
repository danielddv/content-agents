"""Transcribe un vídeo o audio en local (gratis) con faster-whisper.

Uso:
    python -m tools.transcribe VIDEO --out transcript.json [--model small]

Guarda un JSON con segmentos y palabras con tiempos, y un .txt legible con marcas de tiempo.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def fmt(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def transcribe(media: Path, out: Path, model_size: str = "small", language: str = "es") -> dict:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segments, info = model.transcribe(str(media), language=language, word_timestamps=True, vad_filter=True)
    data = {"source": str(media), "language": info.language, "duration": info.duration, "segments": []}
    for seg in segments:
        data["segments"].append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
            "words": [{"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word.strip()}
                      for w in (seg.words or [])],
        })
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    out.with_suffix(".txt").write_text(
        "\n".join(f"[{fmt(s['start'])} - {fmt(s['end'])}] {s['text']}" for s in data["segments"]),
        encoding="utf-8",
    )
    return data


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("media", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--model", default="small", help="tiny, base, small, medium, large-v3 (más grande = mejor y más lento)")
    p.add_argument("--language", default="es")
    a = p.parse_args()
    data = transcribe(a.media, a.out, a.model, a.language)
    print(f"Transcripción lista: {len(data['segments'])} segmentos, {data['duration']:.0f} s → {a.out}")


if __name__ == "__main__":
    main()
