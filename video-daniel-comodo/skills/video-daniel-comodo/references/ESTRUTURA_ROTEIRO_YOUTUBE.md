# Estrutura de roteiro: vídeos de 5 minutos no YouTube (Daniel IA)

Base: o fluxo dos podcasts (`Claude\podcasts`, leitor → roteirista → validador) adaptado para vídeo solo de 5 minutos com o clone do Daniel na HeyGen e a voz da ElevenLabs. Escrito em 18/11/2026.

## 1. O que o YouTube recompensa (e o que muda no roteiro)

| O que pesa | O que significa | O que o roteiro faz |
|---|---|---|
| Os primeiros 30 segundos | O YouTube Studio mostra quanto do público passou dos 30 s ("Intro"). É ali que a maioria sai. | Gancho em 3 blocos de 10 s, sem vinheta, sem "olá, pessoal" e sem apresentação antes do problema. |
| Promessa cumprida | Título e thumbnail chamam o clique; se o começo não entrega o que prometeram, o público sai e o vídeo perde força. | O gancho repete a promessa do título com outras palavras e entrega a primeira resposta antes de 1:10. |
| Retenção ao longo do vídeo | As quedas acontecem quando o assunto fica igual por muito tempo. | Um "re-gancho" a cada 60 a 90 s (novo passo, nova pergunta) e uma mudança visual a cada 8 a 15 s. |
| Satisfação | O YouTube diz que busca satisfação do público, não só minutos assistidos. | Nada de enrolação: toda promessa aberta é fechada (payoff) e o vídeo termina com algo para fazer. |
| Shorts como porta de entrada | Canais que unem Shorts e vídeos longos tendem a crescer mais na maioria dos nichos. | Cada passo é escrito para virar um Short sozinho (começa com uma frase que se sustenta). |

Os números de mercado sobre retenção (porcentagens "ideais", limites do algoritmo) vêm de blogs de ferramentas e não são oficiais. A régua é a média do próprio canal: mudar uma coisa por vídeo e comparar.

## 2. A estrutura (5 min, cerca de 800 palavras)

Ritmo da voz do Daniel na ElevenLabs: cerca de 165 palavras por minuto (720 palavras deram 4 min 22 s). Para 5 minutos, mire **780 a 830 palavras**.

| Cena | Tempo | Palavras | Função |
|---|---|---|---|
| 1. Gancho | 0:00 a 0:30 | 70 a 85 | Bloco 1 (10 s): a dor concreta que confirma o título. Bloco 2 (10 s): por que importa. Bloco 3 (10 s): o que o vídeo vai mostrar + uma promessa aberta específica ("a terceira é a mais difícil"). |
| 2. Virada | 0:30 a 1:05 | 85 a 100 | A crença comum contra a ideia central do ebook. Fecha dizendo o objetivo dos passos. Sem apresentação do Daniel ("Eu sou o Daniel, da Cômodo" soou forçado, retirado em 19/11/2026): o nome entra na tela, não na fala. |
| 3a. Passo 1 | 1:05 a 2:05 | 140 a 160 | Mini-gancho (pergunta) → o erro comum → o que fazer (frase ou script do ebook) → "na prática". |
| 3b. Passo 2 | 2:05 a 3:05 | 140 a 160 | Começa ligando ao passo anterior ("O cliente respondeu. E agora?"). Mesma estrutura. |
| 3c. Passo 3 | 3:05 a 4:10 | 150 a 170 | Fecha a promessa aberta do gancho ("o que eu prometi lá no começo"). É o passo mais forte. |
| 4. Ligação | 4:10 a 4:35 | 50 a 70 | O que os três passos têm em comum: a ideia central de novo, agora com prova. |
| 5. Ação + chamada | 4:35 a 5:00 | 80 a 100 | Uma tarefa para amanhã (do próprio ebook), a chamada para o ebook com link na descrição e uma pergunta para os comentários. |

### Regras de cada cena
- **Gancho:** começa no meio do problema ("Você responde o cliente certinho no WhatsApp, ele visualiza... e some."). Proibido abrir com nome, saudação, logo ou "neste vídeo".
- **Promessa aberta:** no máximo 2 por vídeo, sempre específicas, e todas fechadas antes da cena 5. "Fica até o final" sozinho não serve.
- **Passos numerados:** aqui pode (é diferente do podcast). Viram capítulos e Shorts. Sempre 3 passos: cabe em 5 minutos e o público lembra.
- **Cada passo começa com uma frase que se sustenta sozinha**, para o corte do Short não precisar de contexto.
- **Uma ideia por frase.** Frases curtas. Pergunta antes da resposta.
- **Fechamento:** uma só chamada (o ebook) e uma só pergunta para comentar. Os últimos 20 s ficam livres para a tela final do YouTube.

## 3. O que vem igual do podcast (não muda)
- **Fidelidade:** nenhum número, caso, pesquisa ou resultado que não esteja no ebook. Opinião do Daniel sempre marcada ("eu acho", "na minha leitura").
- **O Daniel nunca cita cargo** e não inventa experiência da Cômodo ("na Cômodo a gente vê...").
- **Fala sobre o assunto, não sobre o livro:** no máximo 3 menções ao ebook fora da chamada final.
- **Pronto para voz:** números por extenso ("vinte e quatro horas"), sem colchetes, sem travessão, sem siglas difíceis. Exemplos de mensagem entre aspas, sem campos como [nome].
- **O Daniel conversa com quem assiste:** "pensa comigo", "repara", "sabe aquele...".

## 4. Formato do arquivo (pronto para edição)
Um arquivo `roteiro_5min.txt`, com uma linha de cabeçalho por cena e o texto falado logo abaixo:

```
## CENA 3a | Passo 1: nome do passo | 1:05 a 2:05 | TELA: texto curto na tela | ANIMAÇÃO: o que encenar | SHORT: sim
Texto falado da cena...
```

- **TELA:** até 6 palavras, a frase que o espectador precisa lembrar.
- **ANIMAÇÃO:** encena o que está sendo dito (pessoas, celular, loja, calendário), não metáfora abstrata. Em vídeo orgânico, WhatsApp aparece só como logo e ícones, nunca como conversa simulada.
- **SHORT: sim** marca cenas que viram corte vertical.
- O texto que vai para a ElevenLabs é só o texto falado (sem as linhas `##`).

## 5. Pacote que acompanha cada roteiro (`pacote.md`)
1. **3 opções de título** (até 60 caracteres, com a dor do lojista e uma promessa concreta).
2. **Texto da thumbnail:** 2 a 4 palavras, diferente do título, com o rosto do Daniel.
3. **Capítulos** com os tempos das cenas (mínimo 3, cada um com 10 s ou mais).
4. **Descrição:** 2 linhas sobre o vídeo + link do ebook na primeira linha visível.
5. **3 cortes para Shorts:** cena, tempo e a primeira frase do corte.
6. **Comentário fixado:** a pergunta da cena 5.

## 6. Como medir depois de publicar
No YouTube Studio, para cada vídeo:
- **Intro (retenção aos 30 s):** se cair, o gancho não confirmou o título.
- **Quedas no gráfico:** anotar o minuto e a cena do roteiro. Queda no meio de um passo = explicação longa demais.
- **Duração média e taxa de cliques:** clique alto com duração baixa = título prometeu mais do que o vídeo entrega.
- Mudar **uma coisa por vídeo** (tipo de gancho, ordem dos passos, título) e comparar com a média do canal.

## 7. Checklist do roteiro
- [ ] Gancho começa no problema e confirma o título em até 10 s.
- [ ] Promessa aberta específica no gancho e fechada no passo 3.
- [ ] Sem "Eu sou o Daniel, da Cômodo" na fala (o nome vai na tela).
- [ ] 3 passos, cada um com erro comum, o que fazer e "na prática".
- [ ] Um re-gancho a cada 60 a 90 s.
- [ ] Tudo o que é fato está no ebook; opinião marcada.
- [ ] 780 a 830 palavras; números por extenso; sem colchetes nem travessão.
- [ ] No máximo 3 menções ao ebook fora da chamada final.
- [ ] Uma chamada só e uma pergunta para comentar.
- [ ] Pacote completo: títulos, thumbnail, capítulos, descrição, Shorts.

## Fontes da pesquisa
- vidIQ, retenção de público: https://vidiq.com/blog/post/audience-retention-secrets-youtube/
- Teleprompter.com, retenção: https://www.teleprompter.com/blog/youtube-audience-retention
- OutlierKit, ganchos e retenção no meio do vídeo: https://outlierkit.com/resources/youtube-hooks-and-retention/
- OutlierKit, sinais de satisfação: https://outlierkit.com/resources/youtube-viewer-satisfaction-algorithm-2026/
- Shopify, como o algoritmo funciona: https://www.shopify.com.au/blog/youtube-algorithm
- AIR Media-Tech, Shorts e vídeos longos (18 mil canais): https://air.io/en/audience-growth/do-youtube-shorts-help-your-long-form-videos-grow-data-from-18000-channels
- vidIQ, cortar vídeo longo em Shorts: https://vidiq.com/blog/post/Clip-youtube-videos-long-to-short/
