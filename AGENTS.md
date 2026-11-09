# Reglas compartidas para agentes de código (Claude Code, Codex)

## Proyecto
Agentes de IA que editan contenido: vídeos para redes sociales (`agents/video_editor`)
y textos de blog (`agents/blog_editor`). Lenguaje: Python 3.11+.

## Contrato de eventos (no romperlo)
Todo agente registra lo que hace con `core.events.EventLog`, que escribe una línea JSON
por evento en `runs/<run_id>/events.jsonl`. El panel (`panel/`) depende de este formato:

```json
{"ts": "2026-11-09T12:00:00+00:00", "run_id": "...", "agent": "blog_editor",
 "type": "step", "message": "Corrigiendo ortografía", "data": {}}
```

Tipos de evento: `start`, `step`, `edit` (con `data.before` y `data.after`),
`artifact` (con `data.path` a un archivo generado), `error`, `done`.

## Reparto de trabajo
- Agentes y herramientas: `agents/`, `tools/`, `core/`.
- Panel web: `panel/`. Solo lee `runs/`; nunca modifica la salida de los agentes.

## Convenciones
- Mensajes de commit claros, en español.
- No subir `runs/`, vídeos ni claves de API (usar variables de entorno).
