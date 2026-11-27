# Comece aqui — vídeos do Daniel em 2 textos

Você não precisa saber programar. Cole o **Texto 1** uma vez e depois use o **Texto 2** sempre que quiser um vídeo. O Claude faz o resto e pede seu OK antes de gastar créditos.

## Antes de começar (peça ao João)
1. **Acesso a este repositório**: o convite chega no seu e-mail do GitHub. Aceite o convite.
2. **Chaves da Cômodo** (ElevenLabs, HeyGen e os ids das vozes), por um canal privado. Você só cola no arquivo `.env` quando o Claude abrir. **Nunca cole chave no chat.**
3. App **Claude** instalado, usando a aba **Code**.

## Texto 1 — instalar (cole uma vez só, na aba Code)
```
Quero fazer vídeos do Daniel com os plugins da Cômodo.
1. Instale o marketplace jccomodo/comodo-plugins e os plugins video-daniel-comodo, editor-videos-comodo e validador-videos-comodo. Se você não conseguir instalar sozinho, me diga exatamente onde clicar.
2. Prepare meu computador rodando o setup da skill video-daniel-comodo e me avise se faltar instalar algum programa.
3. Abra o arquivo .env para eu colar as chaves que recebi. Não me peça as chaves no chat.
4. Confira se a HeyGen está conectada na conta da Cômodo.
```
Se o Claude pedir para clicar: **Personalização → Plugins → Adicionar marketplace → `jccomodo/comodo-plugins`**, instale os três plugins. A HeyGen fica em **Personalização → Conectores → HeyGen** (login da conta da Cômodo).

## Texto 2 — pedir um vídeo (troque só o que está entre colchetes)
```
Use a skill video-daniel-comodo.
Formato: [vertical para Reels | horizontal para YouTube | tela dividida | anúncio STORY estilo B]
Voz: [DAN]
Roteiro:
[cole o texto aqui]
Antes de gastar créditos, me diga quanto custa e espere meu OK. No fim, passe o validador e me entregue o MP4.
```

## Pedidos de uma linha
- `Refaça o anúncio [nome] com a voz DAN, aproveitando a edição.`
- `Censure o palavrão do vídeo [nome].`
- `Agora faça a versão tela dividida desse vídeo.`
- `Troque a frase "[frase]" sem regravar tudo.`

## O que acontece depois
1. O Claude grava a narração e manda para você ouvir. Você responde **"aprovada"**.
2. Ele diz quantos créditos da HeyGen vai gastar. Você responde **"pode gerar"**.
3. Ele edita, passa o validador e entrega o MP4 com o custo.

## Custo de referência
- Narração: ≈ 1 crédito ElevenLabs por caractere (1 min ≈ 1.000).
- Vídeo do Daniel (HeyGen Avatar 6 Turbo): ≈ 20 créditos por minuto.
- Edição, tela dividida, anúncio, censura e validador: 0 crédito.
