# Plugins do Claude da Cômodo

Marketplace privado com os plugins de vídeo da Cômodo:

- **video-daniel-comodo**: vídeos com o clone de IA do Daniel nos formatos A (horizontal), B (vertical) e C (tela dividida); voz na ElevenLabs, vídeo na HeyGen. Veja `video-daniel-comodo/LEIA-ME.md`.
- **editor-videos-comodo**: edição no padrão do time (reels/ADS CMDxxx, legenda padrão, zooms, motions, LUT) e decupagem com cortes suaves para o Premiere. Veja `editor-videos-comodo/LEIA-ME.md`.
- **validador-videos-comodo**: validador crítico que escreve o laudo GRAVE/MÉDIO/LEVE antes da entrega. Veja `validador-videos-comodo/LEIA-ME.md`.

## Adicionar no Claude
No app Claude: Personalização → Plugins → Adicionar → marketplace → `jccomodo/comodo-plugins`. Depois instale os plugins que for usar (`video-daniel-comodo`, `editor-videos-comodo`, `validador-videos-comodo`).
No terminal `claude`:
```
/plugin marketplace add jccomodo/comodo-plugins
/plugin install video-daniel-comodo@comodo
/plugin install editor-videos-comodo@comodo
/plugin install validador-videos-comodo@comodo
```
É preciso ter acesso a este repositório privado no GitHub.
