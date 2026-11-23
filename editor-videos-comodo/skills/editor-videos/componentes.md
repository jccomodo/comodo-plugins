# Componentes

## Padrão medido (2026-10-13) — prevalece sobre as estimativas mais abaixo

Medido em `CMD114 - STORY` (44 s), `CMD086` e `CMD087`, com rastreio de rosto e análise de quadros. Detalhes e números em `SKILL.md` (regras 5 a 10).

- **Pilha cinética:** linhas empilhadas, entrelinha apertada, tamanhos por papel (normal Bold ~88; rótulo ExtraBold ~100 vermelho; palavra-chave ExtraBold ocupando ~60–70% da largura). Exemplos vistos: "chega uma hora / em que você / **precisa** / decidir em que / **velocidade** / quer jogar"; "perdendo / **lead** / para quem responde"; "no dia / **28**"; "um treinamento / ao vivo / **online** / 100% gratuito".
- **Título de abertura em MAIÚSCULAS:** "DONO DE / LOJA (enorme, branco com leve degradê) / DE PLANEJADOS (vermelho)".
- **Logotipo no topo, acima da cabeça:** "MASTERCLASS" em fonte condensada (Tusker), branco, ~85% da largura.
- **Legenda corrida:** palavra isolada, Poppins Medium ~64–74 px, branca, y≈80% da altura.
- **CTA:** "CLICA / [NO BOTÃO em pílula vermelha] / ABAIXO", maiúsculas ExtraBold, fundo escurecido.
- **Cor:** branco puro e vermelho/laranja da marca, ambos sob a LUT.
- **Enquadramento:** nariz fixo em (50%, 44%); só o fundo muda no zoom.

Todos em **Poppins**. Valores de tamanho e tempo abaixo são **pontos de partida estimados** a partir de quadros de baixa resolução (1 a 2 s de amostragem); calibrar comparando com os vídeos de referência. Coordenadas para canvas 1080×1920.

Pesos prováveis (não confirmados): frase de apoio SemiBold/Bold; palavra laranja de destaque Bold/ExtraBold; números gigantes ExtraBold/Black; texto da pílula SemiBold/Bold.

## Destaque (gancho de frase)
- Duas camadas centralizadas na altura do peito: linha de apoio pequena em branco em cima, palavra-chave grande em **laranja** embaixo ("existe uma pergunta / **gratuita**").
- Palavra-chave é substantivo, adjetivo ou número, nunca artigo ou preposição.
- Pode ter três níveis ("um evento / 100% online / **e gratuito**"). Máximo de 3 linhas.
- Entra e sai em sincronia com a fala; sair antes da próxima frase começar.

## Pílula
- Retângulo arredondado laranja Cômodo, texto branco pequeno, centralizado.
- 1 a 3 palavras por vez, trocando a cada ~1 s no ritmo da fala.
- No perfil Gancho: sobre o peito. No perfil Tela dividida: sobre a linha de divisão.
- Frases de ligação e marcadores ("ninguém faz", "a maioria", "das lojas"), não frases de impacto.

## Legenda corrida (perfil Explicação)
- Branca, pequena, sem fundo, 1 a 2 palavras por vez, centralizada no peito.
- Sem animação pesada. Palavra decisiva pode ficar laranja e maior ("vai **estar**").
- Garantir contraste sobre a camiseta preta; sombra suave se necessário.

## Número gigante
- Dado ou número da fala ("**3**", "**60%**", "dia 29") em branco, ocupando boa parte da largura; contexto menor em volta ("por", "dos clientes de **planejados**").
- Entra com impacto curto (scale), a legenda normal sai de cena enquanto ele aparece.
- Usado no perfil Gancho. Um número por vez.

## Zoom de ênfase
- Zoom digital sobre o rosto no gancho, com o número gigante em cima (CMD114, ~3 s).
- Em Explicação o enquadramento já é mais fechado; zoom leve pontual permitido.

## Flash de transição
- Preenchimento laranja translúcido que clareia o quadro por poucos quadros, fechando o gancho (CMD114, ~6 s). Só no perfil Gancho.

## Selo circular com foto
- Círculo com borda/fundo laranja, foto da pessoa citada, no canto superior direito do rosto.
- Pílula com o nome logo abaixo ("Anderson Angeoli"). Foto fornecida pelo usuário; nunca gerar rosto.

## Layout dividido
- Topo ~40% da altura, fundo branco, imagem de apoio centralizada e legível; fixa do 1º segundo ao último.
- Base ~60%, apresentador enquadrado bem fechado.
- Linha de divisão é onde a pílula fica.

## Abertura com blur
- Primeiros ~0,5 s: rosto ampliado e desfocado que faz zoom out e nitidez até o enquadramento normal.

## Cartão do Instagram (CTA)
- Barra branca arredondada com ícone/avatar, @ do perfil e botão "Seguir". O botão muda de cor (clique simulado).
- Entra por cima da legenda nos últimos ~4 s.
- No perfil Tela dividida/Explicação o vídeo fecha em preto com o cartão no centro.
- O @ ainda precisa ser confirmado com o usuário.

## CTA em texto (Gancho)
- "link na bio" em branco e "para **cadastrar**" com a palavra em laranja, dois níveis, fixo no peito até o fim.
