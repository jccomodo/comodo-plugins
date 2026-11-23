# Plugin validador-videos-comodo

Revisa um vídeo antes da entrega e aponta o que o cliente costuma reclamar. Mede sobreposição, texto apertado, margens e zona segura de ADS, elementos cortados, legenda coberta, sincronia com a fala e loop. Depois confere os quadros contra o checklist da Cômodo.

O validador não corrige nada. Ele escreve um laudo em `val\laudo.md`, dentro da pasta do vídeo, com cada problema marcado como GRAVE, MÉDIO ou LEVE, com o tempo e a evidência.

## Instalar
No Claude, abra Personalização → Plugins → Adicionar, adicione o marketplace **jccomodo/comodo-plugins** e instale `validador-videos-comodo`.

Ele precisa de Python com `playwright` e `pillow`. O setup dos plugins `editor-videos-comodo` ou `video-daniel-comodo` já instala os dois.

## Usar
Peça, por exemplo: "Valida o vídeo C:\...\CMD240_FINAL.mp4 (HTML da animação em ...)".

O Claude roda o agente `validador-videos` e resume os problemas GRAVE e MÉDIO. Corrija esses e rode o validador de novo antes de entregar.
