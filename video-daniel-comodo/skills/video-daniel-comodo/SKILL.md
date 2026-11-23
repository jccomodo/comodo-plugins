---
name: video-daniel-comodo
description: Gera vídeos com o clone de IA do Daniel (Cômodo) — narração com a voz dele na ElevenLabs, vídeo na HeyGen com Avatar 6 Turbo (cenário original ou estúdio "Podcaster"), troca de frases soltas sem regravar tudo e entrega do MP4. Usar sempre que alguém da Cômodo pedir "um vídeo do Daniel", "gerar com o clone", "narrar com a voz do Daniel", "gerar as cenas na HeyGen", "trocar só essa frase do áudio", vídeos de YouTube de 5 min dos ebooks ou vídeos curtos (avisos, brincadeiras, testes do avatar), mesmo sem dizer "skill".
---

# Vídeos do clone do Daniel (ElevenLabs + HeyGen)

Quem usa: qualquer pessoa da Cômodo, sem saber programar. Você (Claude) faz tudo; a pessoa aprova o texto, o áudio e o gasto.

Ordem fixa: **texto → narração → aprovação do áudio → vídeo → conferência → entrega**. Nunca gerar o vídeo antes de a pessoa aprovar o áudio: áudio é barato de refazer, vídeo não.

Pastas: os scripts ficam em `scripts/` ao lado deste SKILL.md (`<pasta desta skill>`). O trabalho e o `.env` ficam em `Comodo-Videos-Daniel` na pasta pessoal (Windows `%USERPROFILE%\Comodo-Videos-Daniel`; Mac `~/Comodo-Videos-Daniel`). Cada vídeo numa subpasta com nome curto (ex.: `glow-up`). Nunca em Downloads.
Python: no Windows `python` (ou `py`), no Mac `python3`.

## 0. Preparar o computador (só na 1ª vez)
1. Windows: `powershell -ExecutionPolicy Bypass -File "<pasta desta skill>\setup.ps1"`. Mac: `bash "<pasta desta skill>/setup.sh"`.
2. Se avisar FALTA INSTALAR, peça para a pessoa instalar o que faltou e rode de novo.
3. Se avisar FALTA A CHAVE: abra o `.env` para a pessoa (Windows `notepad "%USERPROFILE%\Comodo-Videos-Daniel\.env"`; Mac `open -e ~/Comodo-Videos-Daniel/.env`) e peça para colar as chaves **da Cômodo** (ElevenLabs, id da voz "Daniel v4", HeyGen) e salvar. **Nunca** peça chave no chat, nunca leia, imprima ou copie os valores do `.env`.
4. Conector da HeyGen: precisa estar conectado no Claude (Personalização → Conectores → HeyGen) **na conta da Cômodo**, com login feito pela própria pessoa. Confira com `get_current_user`; se a conta não for a da Cômodo, pare e avise.

## 1. Texto
- Se a pessoa mandar um texto base, **seguir o texto base** (só ajustar pontuação para pausas). Não reescrever sem pedir.
- YouTube 5 min: siga `references/ESTRUTURA_ROTEIRO_YOUTUBE.md` (gancho 3×10 s, sem auto-apresentação, 3 passos, 780–830 palavras). Cada cena começa com `## CENA N | ...`.
- Não usar "Eu sou o Daniel, da Cômodo" (soa forçado).
- Pausas: reticências `...` e linhas em branco. Pausa longa (piada, suspense) se ajusta depois (passo 3).

## 2. Narração (ElevenLabs — pedir OK do custo antes)
Custo ≈ 1 crédito ElevenLabs por caractere: diga o total antes de gerar.
```
node "<pasta desta skill>/scripts/narrar.js" ROTEIRO.txt --saida PASTA/audio --style 0.5
```
- Com `## CENA` → um MP3 por cena (`--so 3` refaz só a cena 3; `--pular 1,2`). Sem cabeçalhos → `narracao.mp3`.
- Ajustes aprovados:
  - YouTube, explicação com emoção: `--style 0.5`.
  - Fala firme, menos feminina: `--stability 0.35 --style 0.15`.
  - Frase que ficou forçada/exagerada: regravar só ela com `--stability 0.5 --style 0`.
- Mandar o áudio para a pessoa ouvir. Gerar uma variação por vez; apagar as descartadas quando ela escolher.

## 3. Trocar uma frase sem regravar tudo
1. Tempo de cada palavra: `python scripts/transcrever.py narracao.mp3`.
2. Frase nova com contexto (mantém a entonação):
   `node scripts/narrar.js --frase "e eu acabei de ganhar." --antes "frase anterior" --depois "frase seguinte" --saida trecho.mp3 --stability 0.5 --style 0`
3. Emendar (tira o silêncio, iguala o volume, fades curtos):
   `python scripts/emendar.py narracao.mp3 trecho.mp3 INICIO FIM nova.mp3 --antes 0.25 --depois 0.25`
   INICIO/FIM no silêncio entre palavras. Para alongar uma pausa, aumente `--depois`.
4. Ouvir a emenda antes de entregar.

## 4. Vídeo na HeyGen (pedir OK dos créditos antes)
Sempre **Avatar 6 Turbo** (20 créditos/min ≈ 7 créditos a cada 20 s). Avatar 6 Pro custa o dobro: só se a pessoa pedir.

| Cenário | avatarId | reference_look_id |
|---|---|---|
| Original (look "Daniel – 55") | `67cdf4fd28ed46a6819f7cebf3cdadd1` | (não precisa) |
| Estúdio podcast ("Podcaster in blue shirt") | `28c10c546533472ca3da7ed6446631ca` | `67cdf4fd28ed46a6819f7cebf3cdadd1` |

"Com cenário" = estúdio Podcaster. Sem dizer nada = perguntar qual dos dois.

1. `create_asset_upload_batch` com `{filename, content_type: "audio/mpeg", size_bytes}` (tamanho exato do arquivo).
2. PUT do arquivo no `upload_url` com os headers devolvidos:
   `curl -s -o /dev/null -w "%{http_code}" -X PUT -H "content-type: audio/mpeg" -H "x-amz-server-side-encryption: AES256" --data-binary @ARQUIVO "UPLOAD_URL"` → 200.
3. `complete_asset_batch` com o batch_id.
4. `create_video_from_avatar`: `avatarId`, `audioAssetId`, `engine: {"type": "heygen-avatar-6-turbo"}` (+ `reference_look_id` no estúdio), `aspectRatio: "16:9"`, `resolution: "1080p"`, `title`.
5. Em segundo plano: `python scripts/baixar_video.py VIDEO_ID PASTA/video.mp4` (só consulta e baixa). Se der timeout, `get_video` com o id. **Nunca recriar o vídeo para "ver se anda".**
6. Conferir um quadro (`ffmpeg -ss 5 -i video.mp4 -frames:v 1 quadro.jpg`) e a sincronia boca/áudio antes de entregar.

Vídeos longos: **uma cena por áudio** (cada `cena_XX.mp3` vira um vídeo). Se uma sair ruim, refaz só ela. Para juntar cenas use o filtro concat do ffmpeg (nunca `-c copy`: dá deriva de áudio) e normalize o áudio final em −14 LUFS para YouTube. Textos na tela de vídeos do YouTube: nada em caixa alta.

## O que não fazer (já reprovado)
- Fundo verde/chroma para recortar o Daniel. Cenário novo = look feito na HeyGen (Look Studio), nunca recorte.
- Enviar foto de cenário para a HeyGen ou criar look só por texto.
- Avatar 6 Pro sem pedir; API paga de imagem sem pedir.
- Criar conta ou digitar senha: a pessoa faz o login.

## Fechamento
No fim diga onde está o MP4 e o custo: caracteres ElevenLabs e créditos HeyGen (antes/depois via `get_current_user`).
