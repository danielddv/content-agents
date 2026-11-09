---
name: preparar
description: Comprueba e instala en el ordenador lo que necesitan los agentes (Python, FFmpeg, faster-whisper). Úsalo la primera vez en un ordenador nuevo. Uso - /preparar
---

El usuario no es programador: explica cada paso en una frase y pide permiso antes de instalar nada.

1. Detecta el sistema operativo (macOS, Windows o Linux).
2. Comprueba: `python3 --version` (o `python --version` en Windows; hace falta 3.11 o superior) y `ffmpeg -version`.
3. Si falta algo, instálalo:
   - macOS: Homebrew (`brew`); si no está, guíale para instalarlo desde https://brew.sh. Luego `brew install python ffmpeg`.
   - Windows: `winget install Python.Python.3.12` y `winget install Gyan.FFmpeg`. Puede hacer falta cerrar y abrir la app.
   - Linux: `sudo apt install python3 python3-pip ffmpeg`.
4. Instala las dependencias del proyecto: `python3 -m pip install -e ".[video]"`.
5. Prueba que todo funciona: `python3 -m tools.video --help` y un `python3 -c "import faster_whisper"`.
   La primera transcripción descargará el modelo de voz (unos 500 MB, solo una vez).
6. Explícale cómo usar los comandos: `/video-a-contenido`, `/pulir-clip`, `/blog`, `/nueva-marca`.
