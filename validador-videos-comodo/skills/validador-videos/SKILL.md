---
name: validador-videos
description: Valida um vídeo/animação da Cômodo (Reels/ADS estilo D, CMDxxx) antes da entrega, caçando os microdetalhes que o cliente sempre aponta - ícone ou texto coberto por linha/borda, escrita apertada ou vazando do card, conteúdo fora da margem (orgânico ou zona segura de ADS), elemento cortado por zoom/máscara/borda, legenda coberta, tachado fora do meio, zoom sem sentido, logo errado, sincronia com a fala, loop e áudio. Usar SEMPRE depois de renderizar um vídeo e antes de dizer que está pronto, e quando o usuário pedir para validar/revisar/conferir um vídeo.
---

# Validador de vídeos da Cômodo

Dois passos, sempre os dois: **medir** (script, objetivo) e **olhar** (checklist visual). Quem valida não corrige: entrega um laudo com o que corrigir, por gravidade, com tempo e evidência.

## 1. Medir (script)

```
python "<pasta desta skill>\scripts\valida_html.py" <video>\<arquivo>.html --modo organico|ads [--passo 0.2]
```

- Serve para qualquer HTML com `window.render(t)` e `window.READY=1` (padrão dos CMD estilo D). Lê `NF` do HTML para a duração (ou `--dur`).
- `--modo ads` = zona segura do Reel ADS: x 64–1016, y 300–1162, e a faixa y 1162–1265 só até x 923. `--modo organico` = margens x 90–990.
- Saída em `<video>\val\`: `relatorio.md`, `achados.json`, `ev_NN.png` (recorte com a caixa rosa no problema e a zona em verde) e `folha_NN.jpg` (um quadro a cada 2 s).
- O que ele mede: OCULTO, TACHADO, APERTADO, MARGEM, BORDA, MASCARA, LEGENDA, LOOP (só orgânico) e avisos de legenda (dígitos, "Comodo" sem acento).
- Para o script ignorar um elemento proposital (ex.: um cursor diferente), adicione `data-val-ignore` nele no HTML.
- Sempre abra as `ev_NN.png` antes de repassar um achado: o script mede bem, mas confirme que é problema visível. Achado de 1 quadro durante troca de cena costuma ser falso.

Se o vídeo não vier de HTML (reel montado no ffmpeg, corte da decupagem, cena do clone), use o script do MP4:

```
python "<pasta desta skill>/scripts/valida_mp4.py" VIDEO.mp4 [--ass legendas.ass] [--lufs -19.5]
```

Ele mede formato, volume (LUFS e pico), quadro preto, silêncio, a 1ª palavra e se o vídeo termina com frase incompleta; com `--ass`, a sincronia de cada palavra da legenda com a fala. Saída em `val/relatorio_mp4.md` e `val/folha_mp4.jpg`. Depois faça o passo 2.

## 2. Olhar (checklist visual)

Abra as folhas de contato e, nos trechos suspeitos, quadros em tamanho real (ffmpeg `-ss T -frames:v 1` no MP4 final, ou `window.render(t)` no HTML). Passe por TODOS os itens de `checklist.md` (lista do que o cliente já apontou) e marque cada um. Itens de elementos que o vídeo não tem (logo, tachado, VS, cartões do estilo D, sfx de logo) ficam como N/A, não como falha.

## 3. Laudo

Escreva `<video>\val\laudo.md`:

```
# Laudo · CMDxxx · <versão> · <data>
Veredito: APROVADO | CORRIGIR
## GRAVE (impede entrega)
- [t=12.4s] <o que está errado> → <correção sugerida, com o elemento/linha do HTML se souber> (ev_03.png)
## MÉDIO
## LEVE
## Conferido e ok
- <itens do checklist que passaram, curtinho>
```

Gravidade: GRAVE = cliente vai ver na hora (sobreposição, corte de texto, margem de ADS, legenda coberta, logo errado, erro de português, áudio errado). MÉDIO = acabamento (apertado, alinhamento fino, zoom estranho, borda). LEVE = gosto/sugestão.

Não aprove com GRAVE aberto. Depois da correção, rode de novo o script e reveja só os pontos corrigidos e a vizinhança.
