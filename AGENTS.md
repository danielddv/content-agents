# Reglas compartidas para agentes de código (Claude Code, Codex)

## Proyecto
Equipo de agentes de Claude Code que edita contenido: vídeos para redes sociales y textos de blog,
para la cuenta personal @danielddv06 y los clientes de la agencia Flying Frames (@flyingframes.studio).
Los agentes viven en `.claude/agents/` y los comandos que los coordinan en `.claude/skills/`.
Las herramientas gratuitas que usan (FFmpeg, faster-whisper) están en `tools/`. Python 3.11+.
No se usan APIs de pago.

## Contrato de eventos (no romperlo)
Todo agente registra lo que hace con `core.events.EventLog` (o desde la terminal con
`python -m tools.log`), que escribe una línea JSON
por evento en `runs/<run_id>/events.jsonl`. El panel (`panel/`) depende de este formato:

```json
{"ts": "2026-11-09T12:00:00+00:00", "run_id": "...", "agent": "blog_editor",
 "type": "step", "message": "Corrigiendo ortografía", "data": {}}
```

Tipos de evento: `start`, `step`, `edit` (con `data.before` y `data.after`),
`artifact` (con `data.path` a un archivo generado), `error`, `done`.

## Reparto de trabajo
- Agentes, comandos y herramientas: `.claude/`, `tools/`, `core/`, `brands/`.
- Panel web: `panel/`. Solo lee `runs/`; nunca modifica la salida de los agentes.

## Convenciones
- Mensajes de commit claros, en español.
- No subir `runs/`, vídeos ni claves de API (usar variables de entorno).
