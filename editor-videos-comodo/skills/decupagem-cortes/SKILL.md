---
name: decupagem-cortes
description: Decupagem e montagem de vídeos falados da Cômodo (gravação real do Daniel ou cenas do clone na HeyGen), com cortes suaves. Transcreve palavra por palavra, marca pausas, repetições (retakes), começos abandonados e muletas, sugere o que cortar, monta o corte com o auto-editor (margens, corte mínimo, transições curtas, crossfade de áudio) e exporta a linha do tempo para o Premiere. Usar quando o pedido for decupar, fazer o primeiro corte, tirar pausas e repetições, juntar cenas, suavizar cortes ou mandar o corte para o Premiere/DaVinci. Reels verticais CMDxxx no padrão do time ficam com a skill editor-videos; gráficos sobre o vídeo, com talking-head-recut.
---

# Decupagem e cortes suaves

Esta skill faz a parte "de ilha de edição": entender o bruto, decidir o que fica e cortar sem pulo. Motions, legendas e cartões vêm depois, com as skills de sempre.

## Ferramentas (todas locais, nada sobe para a internet)
- **auto-editor 31.8.0**: `%USERPROFILE%\Claude\tools\auto-editor\auto-editor.exe` (o setup da skill editor-videos confere; se faltar, baixar a versão Windows em github.com/WyattBlue/auto-editor/releases e salvar nesse caminho). Usar sempre este caminho. A versão do pip (29.x) é antiga e não tem `--smooth` nem `--transition`. Referência das opções: skills `auto-editor`, `auto-editor-transitions`, `auto-editor-export`, `auto-editor-effects`.
- **Decupagem**: `python scripts/decupar.py VIDEO [--modelo medium|large-v3]`. Usa o Whisper local (faster-whisper, modelos já baixados). Medium: cerca de 50 s de processamento por minuto de vídeo na CPU.
- **Conferência**: `watch-skill watch SAIDA --timestamps T1,T2,...` nos pontos de corte.
- ffmpeg para juntar cenas e medir.

## Fluxo A: gravação real (bruto do Daniel)

1. **Decupar.** `decupar.py bruto.mp4` gera `palavras.json`, `frases.json`, `decupagem.md` e `cortes.txt`. Marcas: `PAUSA` (≥ 0,5 s antes da frase), `RETAKE` (frase repetida: fica a última tomada), `FALSO` (começo abandonado), `MULETA` ("né", "tipo", "éé").
2. **Revisar com o usuário.** Mostrar a tabela da `decupagem.md` e confirmar as decisões antes de cortar. A detecção de retake é por semelhança de texto: conferir as sugestões e acrescentar trechos que o usuário quiser tirar (assunto interno, erro de informação).
3. **Cortar.**
   ```bash
   AE="$USERPROFILE/Claude/tools/auto-editor/auto-editor.exe"
   "$AE" bruto.mp4 --edit audio:-30dB --margin 0.12s,0.15s --smooth 0.3s,1s \
     --cut 12.40sec,15.10sec 40.02sec,41.80sec \
     --transition dissolve:0.08sec:0.5sec -anorm ebu -crf 18 --no-open -o corte.mp4
   ```
   - Os trechos de `--cut` vêm do `cortes.txt` (formato `INÍCIOsec,FIMsec`, separados por espaço).
   - Conferir antes com `--preview` (número de cortes, menor trecho, duração final).
4. **Exportar para o Premiere.** Mesma linha, trocando a saída: `--export premiere -o corte.xml` (DaVinci: `--export resolve`). O time abre o XML e ajusta os cortes com a mídia original. Para levar as transições do Premiere com o nome certo: `--export premiere-otio`.
5. **Conferir** (ver checklist abaixo) e só então seguir para zoom, legendas e motions.

## Fluxo B: cenas do clone (HeyGen)

As cenas chegam limpas (sem pausa nem retake). O trabalho é juntar sem pulo:
1. Medir cada cena (`ffprobe`) e conferir que a fala começa e termina inteira (transcrever o começo e o fim se houver dúvida).
2. Juntar na ordem do roteiro com **crossfade de áudio de 30 ms** em cada emenda e **corte seco na imagem**.
3. **Esconder a emenda com troca de enquadramento**: cena ímpar no enquadramento largo, cena par fechada (escala ×1,12 a ×1,17 em torno de um ponto fixo perto do rosto), como o padrão de dois zooms da editor-videos. Em vídeo 16:9, mesma lógica (hyperframes-keyframes para punch-in).
4. Onde entra animação ou tela cheia, usar **corte em J ou L**: o áudio da próxima cena entra 0,2 a 0,4 s antes da imagem (J) ou o áudio continua 0,2 a 0,4 s sobre a imagem nova (L).

## Regras de corte suave (valem para os dois fluxos)
1. **Nunca cortar dentro de palavra.** Corte de entrada 0,08 a 0,12 s antes da primeira palavra; de saída, 0,15 s depois da última (`--margin 0.12s,0.15s`).
2. **Pausa curta fica.** Só cortar pausas ≥ 0,3 s (`--smooth 0.3s`) e nunca deixar trecho menor que 1 s (`,1s`), que vira gagueira visual.
3. **Áudio sempre com crossfade curto** (10 a 30 ms) em todo corte, para não estalar. A transição `dissolve` do auto-editor já cruza o áudio junto.
4. **Imagem: dissolve só curto em cabeça falante** (até 0,1 s, ou seja, 2 a 3 quadros). Dissolve longo em rosto parece fantasma. Pulo grande se esconde com troca de zoom, não com transição.
5. **Retake: fica a última tomada**, que costuma ser a melhor. Se a primeira for melhor, o usuário decide.
6. **Muleta no meio da frase não se corta** (o rosto pula). Só cortar muleta solta no começo ou no fim da frase.
7. **Corte no ritmo da fala**: trocar de enquadramento no início de frase, nunca no meio.
8. **Volume final**: `-anorm ebu` no corte bruto; na finalização, seguir o padrão Cômodo (−19,5 LUFS, como na editor-videos).

## Checklist antes de entregar
- [ ] Transcrever o corte final e comparar com a decupagem aprovada: nenhuma palavra comida no começo ou fim de trecho.
- [ ] `watch-skill watch corte.mp4 --timestamps <pontos de corte>` e olhar os quadros de cada emenda: sem pulo de cabeça sem troca de zoom, sem quadro preto, sem fantasma de dissolve.
- [ ] Ouvir (ou medir) as emendas: sem estalo, sem respiração cortada pela metade.
- [ ] Duração final batendo com o `--preview`.
- [ ] Entregar: `corte.mp4` (prévia), `corte.xml` (Premiere) e `decupagem.md`.

## Aprendizados
- 18/11/2026: teste em 60 s da gravação do Daniel: sem `--smooth`, o auto-editor fazia 17 cortes (o menor de 0,03 s); com `--smooth 0.3s,1s`, 3 cortes, todos de pausa real. O XML do Premiere saiu com 4 trechos.
- 18/11/2026: nas 3 emendas desse teste, o dissolve de 0,08 s não esconde o pulo: a cabeça muda de posição entre os quadros antes e depois do corte. Confirma a regra 4: em gravação real, toda emenda precisa de troca de enquadramento (largo ↔ fechado) ou de uma imagem por cima.
- 18/11/2026: comparar a transcrição do bruto com a do corte gera falsas diferenças (o Whisper transcreve o mesmo trecho de jeitos diferentes em cada passada). Conferir só as palavras em volta de cada ponto de corte, ou ouvir.
