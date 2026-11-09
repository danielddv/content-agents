# panel

Panel web para ver en vivo qué editan los agentes. Pendiente de construir.

Requisitos:
- Lista de ejecuciones (carpetas en `runs/`), la más reciente primero.
- Línea de tiempo de eventos de la ejecución elegida, actualizándose sola.
- Eventos `edit`: mostrar antes/después con las diferencias resaltadas.
- Eventos `artifact`: previsualizar el archivo (reproductor de vídeo, imagen o texto).

Tecnología sugerida: Streamlit (Python). Formato de eventos: ver `AGENTS.md`.
