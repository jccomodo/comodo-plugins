---
name: video-daniel-comodo
description: Gera vídeos com o clone de IA do Daniel (Cômodo) em três formatos — A horizontal 16:9 (vídeo principal do YouTube, estúdio Podcast Horizontal), B vertical 9:16 (Podcast Vertical, celular) e C tela dividida (método C: animações em cima, Daniel embaixo, legenda em pílula laranja na emenda). Narração com a voz dele na ElevenLabs, vídeo na HeyGen com Avatar 6 Turbo, troca de frases soltas sem regravar tudo e entrega do MP4. Usar sempre que alguém da Cômodo pedir "um vídeo do Daniel", "gerar com o clone", "narrar com a voz do Daniel", "versão vertical", "tela dividida", "método C", "formato A/B/C", vídeos de YouTube de 5 min dos ebooks, Shorts/Reels do clone ou vídeos curtos (avisos, testes do avatar), mesmo sem dizer "skill".
---

# Vídeos do clone do Daniel (ElevenLabs + HeyGen)

Quem usa: qualquer pessoa da Cômodo, sem saber programar. Você (Claude) faz tudo; a pessoa aprova o texto, o áudio e o gasto.

Ordem fixa: **texto → narração → aprovação do áudio → vídeo → conferência → entrega**. Nunca gerar o vídeo antes de a pessoa aprovar o áudio: áudio é barato de refazer, vídeo não.

## Os três formatos

| Formato | Para quê | Tamanho | Look da HeyGen | Custo do vídeo |
|---|---|---|---|---|
| **A — Horizontal** (principal) | vídeo de YouTube de 5 min | 16:9, 1920×1080 | Podcast Horizontal | ≈ 7 créditos a cada 20 s |
| **B — Vertical** | Shorts, Reels, Stories | 9:16, 1080×1920 | Podcast Vertical | ≈ 7 créditos a cada 20 s |
| **C — Tela dividida** | Shorts/Reels com explicação visual | 9:16, 1080×1920 | usa o vídeo do **B** | **0 crédito** (montado no computador) |

- Sem dizer o formato: o padrão é **A**. "Vertical", "celular", "Reels", "Shorts" = **B**. "Tela dividida", "método C", "com animação em cima" = **C**.
- O **C sempre parte de um B pronto** (o mesmo áudio). Se não existir o B daquela cena, gere o B primeiro.
- Um corte do A para Shorts NÃO se faz recortando o 16:9: gere o B com o mesmo áudio (recorte perde qualidade e corta o Daniel).

Pastas: os scripts ficam em `scripts/` e `metodo-c/` ao lado deste SKILL.md (`<pasta desta skill>`). O trabalho e o `.env` ficam em `Comodo-Videos-Daniel` na pasta pessoal (Windows `%USERPROFILE%\Comodo-Videos-Daniel`; Mac `~/Comodo-Videos-Daniel`). Cada vídeo numa subpasta com nome curto (ex.: `atendimento-cena1`), com `A/`, `B/` e `C/` dentro quando houver mais de um formato. Nunca em Downloads.
Python: no Windows `python` (ou `py`), no Mac `python3`.

## 0. Preparar o computador (só na 1ª vez)
1. Windows: `powershell -ExecutionPolicy Bypass -File "<pasta desta skill>\setup.ps1"`. Mac: `bash "<pasta desta skill>/setup.sh"`.
2. Se avisar FALTA INSTALAR, peça para a pessoa instalar o que faltou e rode de novo.
3. Se avisar FALTA A CHAVE: abra o `.env` para a pessoa (Windows `notepad "%USERPROFILE%\Comodo-Videos-Daniel\.env"`; Mac `open -e ~/Comodo-Videos-Daniel/.env`) e peça para colar as chaves **da Cômodo** (ElevenLabs, id da voz "Daniel v4", HeyGen) e salvar. **Nunca** peça chave no chat, nunca leia, imprima ou copie os valores do `.env`.
4. Conector da HeyGen: precisa estar conectado no Claude (Personalização → Conectores → HeyGen) **na conta da Cômodo**, com login feito pela própria pessoa. Confira com `get_current_user`; se a conta não for a da Cômodo, pare e avise.
5. Só para o formato C: `pip install playwright pillow numpy` e `python -m playwright install chromium` (o setup já tenta).

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
- O mesmo áudio serve para A, B e C: narra uma vez só.

## 3. Trocar uma frase sem regravar tudo
1. Tempo de cada palavra: `python scripts/transcrever.py narracao.mp3`.
2. Frase nova com contexto (mantém a entonação):
   `node scripts/narrar.js --frase "e eu acabei de ganhar." --antes "frase anterior" --depois "frase seguinte" --saida trecho.mp3 --stability 0.5 --style 0`
3. Emendar (tira o silêncio, iguala o volume, fades curtos):
   `python scripts/emendar.py narracao.mp3 trecho.mp3 INICIO FIM nova.mp3 --antes 0.25 --depois 0.25`
   INICIO/FIM no silêncio entre palavras. Para alongar uma pausa, aumente `--depois`.
4. Ouvir a emenda antes de entregar.

## 4. Vídeo na HeyGen — formatos A e B (pedir OK dos créditos antes)
Sempre **Avatar 6 Turbo** (20 créditos/min ≈ 7 créditos a cada 20 s). Avatar 6 Pro custa o dobro: só se a pessoa pedir.

| Formato | avatarId (look) | reference_look_id | aspectRatio |
|---|---|---|---|
| A — Podcast Horizontal | `28c10c546533472ca3da7ed6446631ca` | `67cdf4fd28ed46a6819f7cebf3cdadd1` | `16:9` |
| B — Podcast Vertical | `bc28aa603072440397c832ec8b3a9c6a` | `67cdf4fd28ed46a6819f7cebf3cdadd1` | `9:16` |
| (antigo) cenário original "Daniel – 55" | `67cdf4fd28ed46a6819f7cebf3cdadd1` | (não precisa) | `16:9` |

O `reference_look_id` (Daniel – 55) faz o clone mexer as mãos e o rosto como o Daniel de verdade. Nunca pedir 9:16 com o look horizontal (a HeyGen corta as laterais): vertical é sempre o look vertical.

1. `create_asset_upload_batch` com `{filename, content_type: "audio/mpeg", size_bytes}` (tamanho exato do arquivo).
2. PUT do arquivo no `upload_url` com os headers devolvidos:
   `curl -s -o /dev/null -w "%{http_code}" -X PUT -H "content-type: audio/mpeg" -H "x-amz-server-side-encryption: AES256" --data-binary @ARQUIVO "UPLOAD_URL"` → 200.
3. `complete_asset_batch` com o batch_id.
4. `create_video_from_avatar`: `avatarId`, `audioAssetId`, `engine: {"type": "heygen-avatar-6-turbo", "reference_look_id": "67cdf4fd28ed46a6819f7cebf3cdadd1"}`, `aspectRatio` da tabela, `resolution: "1080p"`, `title`.
5. Em segundo plano: `python scripts/baixar_video.py VIDEO_ID PASTA/video.mp4` (só consulta e baixa). Se der timeout, `get_video` com o id. **Nunca recriar o vídeo para "ver se anda".**
6. Conferir quadros (`ffmpeg -ss 5 -i video.mp4 -frames:v 1 quadro.jpg`) e a sincronia boca/áudio antes de entregar.

Vídeos longos: **uma cena por áudio** (cada `cena_XX.mp3` vira um vídeo). Se uma sair ruim, refaz só ela. Para juntar cenas use o filtro concat do ffmpeg (nunca `-c copy`: dá deriva de áudio) e normalize o áudio final em −14 LUFS para YouTube. Textos na tela de vídeos do YouTube: nada em caixa alta.

Look novo (outro cenário/roupa): a pessoa cria no Look Studio da HeyGen (referência Daniel – 55, "Retrato" para vertical, "Paisagem" para horizontal, modelo pessoal ligado, ≈ 1 crédito por geração) a partir de um prompt que você escreve; depois `list_avatar_looks` no grupo `becfcd04c73a48998272a0b4011748a7` para pegar o id.

## 5. Formato C — tela dividida (método C)
Layout fixo 1080×1920: **topo 0–960** = animação sobre fundo claro quadriculado; **embaixo 960–1920** = Daniel do formato B ampliado (≈ 1,25×, topo do cabelo ~66 px abaixo da emenda); **legenda** = pílula laranja `#FF3B1E`, Poppins SemiBold 64, 1–3 palavras, centrada na emenda (y = 960), cresce com as palavras.

Tudo pelo script `metodo-c/metodo_c.py` (nada gasta crédito):
```
python "<pasta desta skill>/metodo-c/metodo_c.py" preparar PASTA/B/video.mp4 PASTA/C
python ".../metodo_c.py" daniel PASTA/C --cabelo Y --rosto-x X        (Y, X medidos no guia.jpg × 2)
python ".../metodo_c.py" teste PASTA/C 1.0,4.5,9.2                       (folha_teste.jpg)
python ".../metodo_c.py" quadros PASTA/C
python ".../metodo_c.py" sfx PASTA/C --soft T,T --tick T --swish T
python ".../metodo_c.py" montar PASTA/C PASTA/C/video_C.mp4
```
1. **preparar** transcreve (palavras.json), gera a pílula (chunks.js), copia o `overlay.html` de exemplo e os assets. Corrija grafias no `palavras.json` ("para" falado como "pra", nomes) e rode `chunks PASTA`.
2. **Plano de cenas antes de animar**: escreva frase → o que aparece (quem, o quê, onde). A animação **encena a fala literalmente** (pessoas, balão, loja, moeda, passos numerados), não metáfora abstrata; gráfico só quando a fala cita dado.
3. **Escrever as cenas** em `PASTA/C/overlay.html`. Use o `exemplo_cena.html` como modelo aprovado: motor de molas `P(nome, inicial, [[t, alvo, resposta, amortecimento]])`, `pop()` para posicionar, ícones prontos (`avatar`, `storeI` loja, `bubble`, `dblck` ✓✓, `coin` R$, `tile` número, `chk`, `tagP` etiqueta, logo do WhatsApp). Regras:
   - Cada elemento entra **0,05–0,25 s antes** da palavra, nunca depois. Nenhum trecho > 0,5 s parado (o `pop` já dá uma flutuação leve).
   - Conteúdo dentro de x 90–990 e y 262–930; ícones grandes (avatar ≈ 135 px de raio, blocos ≥ 140 px), com folga ≥ 30 px entre eles.
   - Um elemento sozinho fica no centro do topo (540, 480); contexto de cena anterior esmaece (30–50%).
   - Destaque sempre laranja Cômodo; neutros cinza; só Poppins; texto na tela só com palavras que o Daniel fala.
   - Nada de conversa/print de WhatsApp em vídeo orgânico (só logo e ícones).
4. **teste** em 8–15 tempos-chave e olhar a folha; depois **quadros**, **sfx** (sons leves nas entradas) e **montar** (o áudio sai a −14 LUFS e o script confere a sincronia: deslocamento tem que ser 0,00 s).
5. **Validar antes de entregar**: rodar o agente `validador-videos` (se existir) ou revisar você mesmo os quadros contra: palavra cortada pela pílula, elementos sobrepostos, margem, trecho parado, elemento atrasado.

## O que não fazer (já reprovado)
- Fundo verde/chroma para recortar o Daniel. Cenário novo = look feito na HeyGen (Look Studio), nunca recorte.
- Enviar foto de cenário para a HeyGen ou criar look só por texto sem a pessoa aprovar.
- Recortar o vídeo 16:9 para fazer o vertical.
- Avatar 6 Pro sem pedir; API paga de imagem sem pedir.
- Criar conta ou digitar senha: a pessoa faz o login.

## Fechamento
No fim diga onde está o MP4 e o custo: caracteres ElevenLabs e créditos HeyGen (antes/depois via `get_current_user`). O formato C não gasta créditos.
