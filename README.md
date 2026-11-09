# content-agents

Equipo de agentes de IA para editar contenido de la cuenta personal **@danielddv06** y de los
clientes de **Flying Frames** (@flyingframes.studio).

Los agentes son **agentes de Claude Code**: funcionan con tu suscripción de Claude, sin claves de API
ni pagos extra. El trabajo con vídeo (cortar, quitar silencios, transcribir, subtítulos) lo hacen
programas gratuitos en tu ordenador (FFmpeg y Whisper).

## Cómo se usa

Abre este proyecto en la app de escritorio de Claude Code y escribe uno de estos comandos:

| Comando | Qué hace |
|---|---|
| `/preparar` | La primera vez: instala lo necesario en el ordenador. |
| `/video-a-contenido video.mp4 marca` | De un vídeo largo saca 3-5 clips verticales con subtítulos, sus textos para redes y un artículo de blog. **Te enseña el plan y espera tu aprobación antes de montar.** |
| `/pulir-clip video.mp4 marca` | Pule un clip corto en bruto: quita silencios, lo pasa a vertical con subtítulos y escribe sus textos. |
| `/blog archivo-o-tema marca` | Escribe o mejora un artículo de blog. |
| `/nueva-marca` | Crea el perfil de un cliente nuevo haciéndote preguntas. |

## El equipo

```
                 Director (el comando que lanzas)
                          │
   transcribir ──► selector-de-clips ──► ✋ TU APROBACIÓN
                                              │
                    ┌─────────────────────────┼──────────────────┐
                 montador                copywriter         redactor-blog
             (clips 9:16 +            (textos TikTok,            │
              subtítulos)              Reels, Shorts)        corrector
                                                                 │
                                                       revisor ──┘ (si no aprueba, vuelve al redactor)
                                                                 │
                                                                SEO
```

Cada agente está definido en `.claude/agents/` y cada comando en `.claude/skills/`.

## Marcas

- `brands/personal.md`: tu cuenta personal.
- `brands/flying-frames/`: un archivo por cliente de la agencia (plantilla: `_plantilla.md`).

Cada perfil define el tono, las reglas y el estilo de vídeo (subtítulos palabra a palabra o clásicos,
colores, encuadre y si se quitan silencios).

## Dónde queda el resultado

Cada ejecución crea `runs/<id>/` con los clips, los textos y el artículo. Esa carpeta queda en tu
ordenador (no se sube a GitHub porque los vídeos pesan mucho). El panel (`panel/`) lee esa carpeta
para enseñarte en vivo qué está haciendo cada agente.
