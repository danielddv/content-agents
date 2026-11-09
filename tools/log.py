"""Registra un evento para el panel desde la línea de comandos.

Uso:
    python -m tools.log RUN_ID AGENTE TIPO "mensaje" [--antes ARCHIVO --despues ARCHIVO] [--archivo RUTA]

TIPO: start | step | edit | artifact | error | done
"""

from __future__ import annotations

import argparse
from pathlib import Path

from core.events import EventLog


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("run_id"); p.add_argument("agente")
    p.add_argument("tipo", choices=["start", "step", "edit", "artifact", "error", "done"])
    p.add_argument("mensaje")
    p.add_argument("--antes", type=Path); p.add_argument("--despues", type=Path)
    p.add_argument("--archivo")
    a = p.parse_args()

    log = EventLog(a.agente, run_id=a.run_id)
    if a.tipo == "edit":
        log.edit(a.mensaje, before=a.antes.read_text(encoding="utf-8") if a.antes else "",
                 after=a.despues.read_text(encoding="utf-8") if a.despues else "")
    elif a.tipo == "artifact":
        log.artifact(a.mensaje, path=a.archivo or "")
    else:
        log.emit(a.tipo, a.mensaje)
    print(f"evento registrado en {log.path}")


if __name__ == "__main__":
    main()
