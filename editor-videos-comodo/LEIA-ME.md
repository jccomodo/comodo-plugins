# Plugin editor-videos-comodo

Edita os vídeos da Cômodo no padrão do time. Traz duas skills:

- **editor-videos:** reels e ADS verticais (CMDxxx) a partir do vídeo bruto. Corta as pausas, alterna dois zooms, coloca a legenda padrão (Poppins), os motions, a LUT da Cômodo, o cartão do Instagram e as margens de ADS.
- **decupagem-cortes:** transcreve palavra por palavra e marca pausas, repetições e muletas. Depois corta com transições suaves e exporta a linha do tempo para o Premiere ou o DaVinci.

## Instalar (uma vez por computador)
1. No Claude, abra Personalização → Plugins → Adicionar, adicione o marketplace **jccomodo/comodo-plugins** e instale `editor-videos-comodo`.
2. No primeiro pedido, o Claude roda o `setup` da skill. Ele confere o Python e o ffmpeg e instala as bibliotecas (cerca de 300 MB na primeira vez).
3. Só para a decupagem: baixe o **auto-editor 31.8** ou mais novo, versão Windows, em github.com/WyattBlue/auto-editor/releases. Salve em `%USERPROFILE%\Claude\tools\auto-editor\auto-editor.exe`. A versão do pip é antiga e não serve.

## Usar
Exemplos de pedido:
- "Edita o CMD240, o bruto está em ..."
- "Decupa esse vídeo e faz o primeiro corte."

Os vídeos finais vão para `%USERPROFILE%\Claude\ENTREGAS\CMDxxx`.

Antes de entregar, rode o validador. Ele está no plugin `validador-videos-comodo`.

Nada aqui gasta créditos: tudo roda no computador. A única exceção é se você pedir explicitamente um banco de vídeo ou uma imagem gerada por IA.
