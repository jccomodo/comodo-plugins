# Checklist do validador (tudo isto já foi apontado pelo cliente em algum vídeo)

Marque cada item: ok / problema (com tempo) / não se aplica.

## Sobreposição e camadas
- [ ] Nenhuma linha, contorno, borda de card ou risco passa POR CIMA de ícone (ex.: contorno vermelho do "óbvio" cruzando o "VS"; bordas de card cruzando o "=").
- [ ] Pílula/selo não fica atrás de contorno ou de outro card (ex.: "óbvio ✓" atrás da linha).
- [ ] Rótulo de personagem ("VOCÊ") nunca atrás do ícone que ele marca.
- [ ] Nada cobre a legenda; nada encosta nela. Elemento nunca desce até a área da legenda.
- [ ] Texto não fica parcialmente atrás da máscara do título (ex.: "87"/"RELATÓRIO" por baixo de "O começo bom") nem da faixa da legenda (ex.: "VENDA" meio escondido).

## Escrita
- [ ] Texto não está apertado: folga visível entre texto e borda do card/pílula (pílula pequena com padding de 3 px = apertado).
- [ ] Texto não vaza do card (ex.: "0 visitas" passando da borda de baixo do card).
- [ ] Linha de texto longa num card estreito: quebrar em 2 linhas centradas, nunca espremer com fonte minúscula nem deixar sem margem ("Quer conhecer..." colado nas bordas).
- [ ] Português: acentos (Cômodo, você, óbvio, mês), crase, concordância; nada de "Comodo".
- [ ] Números na legenda como foram falados ("nove", não "9"); valores coerentes com a fala.
- [ ] Números de exemplo inventados (87 leads, horários, nomes) sinalizados ao usuário.

## Alinhamento
- [ ] Tachado passa no meio das letras (não embaixo, não em cima).
- [ ] Elementos lado a lado ou empilhados alinhados entre si (ex.: "bom projeto" e "fechar a venda" empilhados no mesmo eixo).
- [ ] Sinais entre palavras ("=", "×", "VS") centrados verticalmente com o texto; não usar "×" solto desalinhado.
- [ ] Texto digitado (input/campo) centralizado no campo.
- [ ] Ponteiros/relógios girando no pivô certo.

## Margens e enquadramento
- [ ] Orgânico: conteúdo entre x 90 e 990.
- [ ] ADS Reels: conteúdo em x 64–1016, y 300–1162; faixa y 1162–1265 só até x 923 (legenda vai nessa faixa, centrada em x≈493). Sem card "Seguir" em ADS.
- [ ] ADS Story: x 64–1015, y 285–1634.
- [ ] Zoom com sentido: zoom só para destacar o que a fala cita; nada de zoom no começo que corta o vizinho (ex.: zoom na proposta A cortando a B antes de ela aparecer). Zoom não pode cortar texto na borda nem jogar conteúdo para baixo do título.
- [ ] Em zoom de cena larga, nada sai da margem (zoom ≤ ~1.05 em conteúdo de 900 px de largura).

## Logo e marca
- [ ] Logo da Cômodo no momento "Na Cômodo...": sublogo (símbolo casinha) centralizado, com pulsação e anéis finos; sem brilho amarelo, sem raios, sem faíscas. Som angelical (sfx_logo.mp3) tocando junto.
- [ ] Título da cena Cômodo é o símbolo, não a palavra "Cômodo" escrita.
- [ ] Logo branca só sobre fundo escuro; logo laranja não pode apagar o acento.
- [ ] Só Poppins (capas: Tusker na head). Cores: laranja #FF3B1E, preto #17130F, verde #1FB866.

## Animação e ritmo
- [ ] A animação encena a fala (pessoa, balão, caminho, objeto citado), não metáfora abstrata; o elemento entra junto da palavra (até ~0,3 s depois).
- [ ] Nenhum trecho parado > ~4 s; sem elementos decorativos flutuando sem função (x, círculos soltos).
- [ ] Exemplos visuais batem com o roteiro (ex.: "e esse puxador?" e não "e esse sofá?" se o roteiro pede).
- [ ] Transições sem piscar, sem elemento sumindo e reaparecendo; nada "pula" de posição.
- [ ] Loop (orgânico): último quadro = primeiro; card Seguir nos últimos 3,6 s, sem colar no CTA.
- [ ] CTA bonito: card com respiro, logo, texto em 2 linhas com palavra-chave em laranja, botão com cursor e clique.

## Áudio
- [ ] Entonação certa em cada trecho (ex.: trecho de exemplos com tom de quem cita exemplos; pergunta com tom de pergunta; primeira frase sem tom errado).
- [ ] Voz sem cortes, cliques ou emendas audíveis nos trechos regravados.
- [ ] Efeitos não cobrem a voz; som do logo no momento do logo.
- [ ] Duração dentro do pedido (ex.: ~1:30; velocidade até 1,3×).
- [ ] Legenda em sincronia com a voz (sem atraso visível).

## Entrega
- [ ] Arquivo final em %USERPROFILE%\Claude\ENTREGAS\CMDxxx com nome CMDxxx_<estilo>_vN(.mp4); capa separada.
- [ ] MP4 abre, duração certa, áudio presente, 1080x1920, 30 fps.

## Sombras e destaque
- [ ] Nada de sombra dura/sólida deslocada (ex.: '0 8px 0 #000' embaixo do '=' parece um segundo círculo escuro). Elementos têm que 'saltar' (popup): sombra suave difusa e, se cruzam linhas/bordas, anel da cor do fundo em volta.
- [ ] Troca de estado (VS → =, número mudando) com 'pop' de escala, não troca seca.
