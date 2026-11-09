"""Registro de eventos que el panel lee para mostrar lo que hace cada agente."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"


class EventLog:
    """Escribe eventos en runs/<run_id>/events.jsonl (una línea JSON por evento)."""

    def __init__(self, agent: str, run_id: str | None = None, runs_dir: Path = RUNS_DIR):
        self.agent = agent
        self.run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]
        self.dir = runs_dir / self.run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "events.jsonl"

    def emit(self, type: str, message: str, **data: Any) -> None:
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "run_id": self.run_id,
            "agent": self.agent,
            "type": type,
            "message": message,
            "data": data,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def start(self, message: str = "Inicio", **data: Any) -> None:
        self.emit("start", message, **data)

    def step(self, message: str, **data: Any) -> None:
        self.emit("step", message, **data)

    def edit(self, message: str, before: str, after: str, **data: Any) -> None:
        self.emit("edit", message, before=before, after=after, **data)

    def artifact(self, message: str, path: str | Path, **data: Any) -> None:
        self.emit("artifact", message, path=str(path), **data)

    def error(self, message: str, **data: Any) -> None:
        self.emit("error", message, **data)

    def done(self, message: str = "Terminado", **data: Any) -> None:
        self.emit("done", message, **data)
