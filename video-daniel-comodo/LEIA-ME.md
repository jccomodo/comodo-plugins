# Plugin video-daniel-comodo

Faz vídeos com o clone de IA do Daniel: você manda o texto, aprova o áudio e recebe o MP4.

## Instalar (uma vez por computador)
1. Tenha o app **Claude** (aba Code), o **Node.js LTS**, o **Python 3** e o **ffmpeg**.
2. Em Personalização → Plugins → Adicionar, adicione o marketplace **comodo** e instale `video-daniel-comodo`.
3. Em Personalização → Conectores, conecte a **HeyGen** com o login da conta da Cômodo.
4. No primeiro pedido, o Claude roda o setup e abre o arquivo `.env` em `Comodo-Videos-Daniel`. Cole ali as chaves da Cômodo (ElevenLabs, id da voz do Daniel, HeyGen) e salve. Não cole chave no chat.

## Usar
Diga, por exemplo: "Faz um vídeo do Daniel, com cenário, falando este texto: ...".
O Claude grava a narração, espera você aprovar, gera o vídeo e entrega o MP4 com o custo.

## Custo de referência
- Narração: ≈ 1 crédito ElevenLabs por caractere (20 s ≈ 300).
- Vídeo (Avatar 6 Turbo): ≈ 7 créditos HeyGen a cada 20 s; 5 min ≈ 100.
