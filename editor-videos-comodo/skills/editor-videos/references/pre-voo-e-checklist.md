# Pré-voo, checklist de entrega e conflitos a resolver

Criado em 2026-10-22 a partir da skill de referência `yt-ddiasmatt-animation` (estrutura: ler histórico antes,
regras fixas curtas, checklist de QA, registro no fim). Nada do `SKILL.md` original foi apagado; o backup está em
`SKILL.md.bak-2026-10-22`.

## 1. Pré-voo (antes de qualquer edição)

1. **Ler as Armadilhas do `SKILL.md` e o bloco datado mais recente.** Quando duas regras divergirem, vale a de data
   mais nova; sem data clara, perguntar antes de interpretar (já é regra do `SKILL.md`).
2. **Confirmar o pedido:** número CMD, frente (**orgânico** x **ADS**), formato (STORY, REELS, FEED), método
   (A cartão atrás da cabeça, B tela dividida, C/D conforme `project_estilos_bcd`), arquivo de origem (bruto
   `Teleprompter-*` ou montagem `CMDxxx.mp4`, regra 14h). Perguntar só o que faltar.
3. **Conferir ferramentas e disco:** `ffmpeg`, Python 3.12, faster-whisper `medium`, espaço livre para o render.
4. **Listar as ideias visuais do roteiro e pedir as fotos** (regra 15) antes de montar. Nunca inventar imagem nem chamar
   API paga sem perguntar.
5. **Prazo apertado não autoriza qualidade menor** (resolução, CRF, pular o validador) sem combinar com o usuário.
6. **Custo antes de rodar:** avisar antes de rotoscope, learn-style ou render em clipe longo.

## 2. Checklist de entrega (todos os itens, nesta ordem)

- [ ] `ffprobe`: duração = `duracao_final`; 1080x1920 (ADS FEED 1080x1350), 30 fps; loudness -19,5 LUFS (faixa -19,5 a -20,5).
- [ ] Legenda **centralizada em x=540**, nítida, sem `\blur` no texto corrido.
- [ ] **Sincronia:** validador roda sobre atrasos e adiantamentos (±0,15 s) contra `palavras.json`; todo desvio corrigido e reconferido.
- [ ] **Zona segura:** orgânico x82-1016 / y254-859 (até x874 / y1517); ADS pelas margens STORY/REELS/FEED. Nada no vermelho.
- [ ] Celular/mockup **nunca cortado** (base ≥ 10 px acima da pílula).
- [ ] Motions: `audit.py` com 0 conflitos e conferência à vista (setas, ordem da fala, folhas de quadros). Sem fade-out.
- [ ] Números lidos pelo Whisper conferidos com 3 configurações e **avisados ao usuário**; correções e dúvidas listadas.
- [ ] Sem palavras alucinadas depois da última fala real (`DROP_AFTER`).
- [ ] Tela final/CTA conforme o padrão da frente (orgânico x ADS).
- [ ] Entrega em `%USERPROFILE%\Claude\ENTREGAS\CMDxxx` (`*_FINAL`); rascunhos em `Claude\videos`.

## 3. Registro (depois de entregar)

- Pedido ou correção nova do usuário: gravar com **data** na memória (`feedback_*`) e, se mudar um padrão, no bloco
  datado do `SKILL.md`. Armadilha nova vai para "Armadilhas".
- Não renderizar de novo sem pedido do usuário; ajuste depois da entrega vai para o código e para a skill.

## 4. Ideias da skill de referência ainda NÃO aplicadas (decisão do usuário)

| Ideia | Origem | Por que está parada |
|---|---|---|
| **Notas faladas para a IA** dentro da gravação ("IA, coloca aqui atrás"): listar como tarefa e cortar a fala | `spoken-notes` | Só vale se o time grava instruções no teleprompter. |
| **Curva de intensidade** (denso no início, descendo, calmo no fim) | `transitions-and-cadence` | Conflita com 14k ("menos é mais", ≈ 1 motion a cada 15-20 s). |
| **Câmera nunca pisca:** entre planos, emenda < 0,6 s ou câmera crua ≥ 3 s | idem | Precisa medir nos CMD aprovados antes de virar regra. |
| **Efeitos sonoros e trilha baixa** | `audio` | A skill atual não mixa som além da voz. |

## 5. Conflitos encontrados no `SKILL.md` (a resolver; nada foi alterado)

1. **`\fs` do ASS:** a regra 2 diz × 1,78 (corrigido em 2026-10-14); "Armadilhas" ainda diz × 1,93.
2. **Motion e a cabeça:** 14e atrás (matte), 14i/14m cartão acima da cabeça, 14n NA FRENTE e morrendo no corte,
   atualização de 2026-10-19 "nada sobre a cabeça". Qual vale por método?
3. **Quantidade de motions:** 14c (> 60% do tempo), 14k (≈ 1 a cada 15-20 s), 14n (≈ 1 por plano).
4. **Legenda:** regras 11-13 (pilha, palavra grande, numerais) x 14l (legenda de designer); a memória diz que B/C/D usam a
   legenda do estilo A.
5. **Mockup do celular:** três versões (tela dividida, painel claro, tela cheia com o Daniel escurecido). A última
   ("CORREÇÃO DEFINITIVA", 2026-10-20) vale, mas as anteriores seguem no texto.
6. **Estilos B/C/D** estão só na memória (`project_estilos_bcd`), não na skill.
7. **Encoding:** o `SKILL.md` não é UTF-8 válido (linhas ~115-117, 157 e 159 têm acentos perdidos). O `Edit` recusa o
   arquivo; qualquer correção precisa de conversão.
