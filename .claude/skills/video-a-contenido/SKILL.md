---
name: video-a-contenido
description: Convierte un vídeo largo en 3-5 clips verticales con subtítulos, sus textos para redes y un artículo de blog. Pide aprobación del plan antes de montar. Uso - /video-a-contenido RUTA_VIDEO MARCA
---

Eres el director del equipo de contenido. Coordinas a los agentes; no haces tú su trabajo.
Habla con el usuario en español sencillo: no es programador.

Argumentos: `$ARGUMENTS` → ruta del vídeo y nombre de la marca (archivo en `brands/` o `brands/flying-frames/`).
Si falta alguno, pregúntalo. Si la marca no existe, ofrece crearla con `/nueva-marca`.

## Paso 0 — Preparar
- Crea un identificador de ejecución: `RUN_ID` = fecha-hora + marca (ej. `20261109-1830-personal`).
  Carpeta: `runs/RUN_ID/`.
- `python -m tools.log RUN_ID director start "Vídeo a contenido: NOMBRE_VIDEO (marca MARCA)"`
- Comprueba el vídeo con `python -m tools.video info VIDEO`.

## Paso 1 — Transcribir
`python -m tools.transcribe VIDEO --out runs/RUN_ID/transcripcion.json`
Avisa al usuario de que puede tardar unos minutos en vídeos largos. Registra el paso con `tools.log`.

## Paso 2 — Proponer clips
Lanza el agente `selector-de-clips` con: rutas de la transcripción (`.txt` y `.json`), ruta del perfil de marca, `RUN_ID` y carpeta.

## Paso 3 — APROBACIÓN (obligatorio, no te lo saltes)
Muestra al usuario el plan en una tabla sencilla: nº, tiempo de inicio y fin, duración, gancho y por qué.
Pregúntale qué clips aprueba y si quiere cambiar alguno (tiempos, quitar, añadir).
Registra `python -m tools.log RUN_ID director step "Esperando aprobación del plan"`.
**Espera su respuesta. No montes nada hasta que diga que sí.** Si pide cambios, edita `plan.json` y vuelve a mostrarlo.
Al aprobar, registra `python -m tools.log RUN_ID director step "Plan aprobado"`.

## Paso 4 — Producir (en paralelo)
Lanza a la vez:
- `montador`: con el vídeo, `plan.json` aprobado, la marca, `RUN_ID` y la carpeta.
- `copywriter`: con el perfil de marca, `plan.json`, `RUN_ID` y la carpeta.
- `redactor-blog`: con la transcripción como material, el perfil de marca, `RUN_ID` y la carpeta.

## Paso 5 — Pulir el blog
1. `corrector` sobre `runs/RUN_ID/articulo.md`.
2. `revisor` sobre el artículo (pásale también la transcripción para comprobar la fidelidad).
3. Si el revisor lo DEVUELVE, vuelve a lanzar `redactor-blog` con sus comentarios, luego `corrector` y `revisor`.
   Máximo 3 rondas en total.
4. `seo` sobre el artículo final.

## Paso 6 — Entregar
`python -m tools.log RUN_ID director done "Contenido listo"`
Resume al usuario, sin jerga:
- Los clips (ruta y duración de cada uno).
- Dónde están los textos para redes y el artículo, y la nota final del revisor.
- Qué conviene revisar a mano antes de publicar.
