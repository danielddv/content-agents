# content-agents

Agentes de IA para editar contenido:

- **video_editor** — vídeos para redes sociales (formato vertical 9:16, cortes, subtítulos).
- **blog_editor** — textos de blog (corrección, estilo, SEO).

Cada ejecución de un agente deja un registro de eventos en `runs/<run_id>/events.jsonl`.
El **panel** (`panel/`) lee esos registros para mostrar en vivo qué está editando cada agente.

## Estructura

```
agents/       agentes (uno por carpeta)
tools/        herramientas compartidas (ffmpeg, subtítulos, texto…)
core/         utilidades comunes (registro de eventos)
panel/        panel web para ver las ediciones
runs/         salida de cada ejecución (no se sube a git)
```

## Requisitos

- Python 3.11+
- FFmpeg instalado en el sistema (para vídeo)

```bash
pip install -e .
```
