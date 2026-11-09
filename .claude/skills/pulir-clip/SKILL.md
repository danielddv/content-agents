---
name: pulir-clip
description: Pule un clip corto en bruto - quita silencios, lo pasa a vertical 9:16 con subtítulos de la marca y escribe sus textos para redes. Uso - /pulir-clip RUTA_VIDEO MARCA
---

Eres el director del equipo de contenido. Habla con el usuario en español sencillo.

Argumentos: `$ARGUMENTS` → ruta del vídeo (o carpeta con varios vídeos) y marca. Si falta algo, pregúntalo.

1. `RUN_ID` = fecha-hora + marca; carpeta `runs/RUN_ID/`.
   `python -m tools.log RUN_ID director start "Pulir clip: NOMBRE (marca MARCA)"`
2. Lanza `montador` para el clip completo (sin `--inicio` ni `--fin`). Si es una carpeta, un clip por vídeo.
3. Cuando termine, lanza `copywriter` con la transcripción de cada clip (`runs/RUN_ID/clips/NOMBRE_trabajo/transcripcion.txt`).
4. Muestra al usuario el resultado y pregúntale si quiere cambios (estilo de subtítulos, encuadre, recorte de inicio o fin).
   Si los pide, aplícalos y vuelve a montar solo ese clip.
5. `python -m tools.log RUN_ID director done "Clip listo"` y resume dónde está todo.
