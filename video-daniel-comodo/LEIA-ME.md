# Plugin video-daniel-comodo

Faz vídeos com o clone de IA do Daniel: você manda o texto, aprova o áudio e recebe o MP4.

## Três formatos
- **A — Horizontal (principal):** 16:9 para o YouTube, Daniel no estúdio (look Podcast Horizontal).
- **B — Vertical:** 9:16 para Shorts e Reels (look Podcast Vertical).
- **C — Tela dividida:** 9:16 com animações em cima, o Daniel embaixo e a legenda em pílula laranja no meio. É montado a partir do B, sem gastar créditos.

## Instalar (uma vez por computador)
1. Tenha o app **Claude** (aba Code), o **Node.js LTS**, o **Python 3** e o **ffmpeg**.
2. Em Personalização → Plugins → Adicionar, adicione o marketplace **jccomodo/comodo-plugins** e instale `video-daniel-comodo`.
3. Em Personalização → Conectores, conecte a **HeyGen** com o login da conta da Cômodo.
4. No primeiro pedido, o Claude roda o setup e abre o arquivo `.env` em `Comodo-Videos-Daniel`. Cole ali as chaves da Cômodo (ElevenLabs, id da voz do Daniel, HeyGen) e salve. Não cole chave no chat.

## Usar
Exemplos:
- "Faz um vídeo do Daniel, formato A, falando este texto: ..."
- "Gera a cena 1 no formato B."
- "Agora faz a versão C (tela dividida) dessa cena."

O Claude grava a narração, espera você aprovar, gera o vídeo e entrega o MP4 com o custo.

## Custo de referência
- Narração: ≈ 1 crédito ElevenLabs por caractere (20 s ≈ 300).
- Vídeo A ou B (Avatar 6 Turbo): ≈ 7 créditos HeyGen a cada 20 s; 5 min ≈ 100.
- Formato C: 0 crédito (usa o vídeo do B).
