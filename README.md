# 8-Puzzle
O 8-Puzzle (ou "Jogo dos Oito") é um quebra-cabeça clássico composto por um tabuleiro 3 × 3 contendo 8 peças numeradas (de 1 a 8) e um espaço vazio. O objetivo é deslizar as peças para reorganizá-las em uma ordem crescente específica, usando o espaço vazio para manobrá-las. Usaremos o algoritmo A* em Python. 


🧩 8-Puzzle Solver com Interface Gráfica (A*)
Aplicação desenvolvida para resolver o problema do 8-Puzzle utilizando o algoritmo de busca A* com heurística de distância de Manhattan, e uma interface gráfica simples feita em Python + Tkinter.

O objetivo do jogo é organizar as peças numeradas de 1 a 8 em um tabuleiro 3x3, deixando o espaço vazio (0) na posição final, como no estado objetivo abaixo:


📁 Estrutura do Projeto
eight_puzzle_gui.py → Arquivo principal com:
Representação do problema (estado, movimentos, verificação de solução)
Implementação do algoritmo A*
Interface gráfica com Tkinter
Você pode adaptar os nomes de arquivos se tiver organizado de outra forma.

⚙️ Tecnologias Utilizadas
Linguagem: Python 3
Interface gráfica: Tkinter (biblioteca padrão do Python)
Algoritmo de busca: A* (A-star)
Heurística: Distância de Manhattan
🚀 Como Executar o Projeto
1. Pré-requisitos
Ter o Python 3 instalado.
Você pode baixar em:
[https://www.python.org/downloads](https://www.python.org/downloads)
Tkinter já vem junto com a instalação padrão do Python na maioria dos sistemas. Caso esteja usando Linux e o Tkinter não funcione, pode ser necessário instalar o pacote de GUI correspondente da sua distro.

2. Clonar o Repositório
No terminal ou cmd:

bash
Copiar

git clone <seu-repositorio.git>
cd <pasta-do-repositorio>
3. Executar a Aplicação
Dentro da pasta do projeto, rode:

bash
Copiar

python eight_puzzle_gui.py
Ou, dependendo da sua instalação:

bash
Copiar

python3 eight_puzzle_gui.py
Uma janela será aberta com o tabuleiro do 8-puzzle.

🖥️ Como Usar a Interface
A interface contém:

Um tabuleiro 3x3 com as peças (botões) representando os números de 1 a 8 e o espaço vazio.
Botões de controle abaixo ou ao lado do tabuleiro.
🧮 Botões principais
"Estado Aleatório"
Gera um tabuleiro aleatório que seja solucionável.
A aplicação verifica inversões para garantir que exista solução.

"Resolver (A*)"
Executa o algoritmo A* a partir do estado atual do tabuleiro.

Usa a distância de Manhattan como heurística.
Se houver solução, o caminho de estados é armazenado.
Se o estado não for solucionável (caso alterado manualmente no código), uma mensagem de erro é exibida.
"Próximo passo"
Avança passo a passo pelos estados da solução encontrada:

Mostra a sequência de movimentos até chegar ao estado objetivo.
Exibe qual passo está sendo mostrado em relação ao total.
"Resetar"
Volta o tabuleiro para o estado objetivo (solução final).

🧠 Lógica do Algoritmo (A*)
Representação do estado
O tabuleiro é representado como uma tupla de 9 elementos, por exemplo:
(1, 2, 3, 4, 5, 6, 7, 8, 0)
Índices:
0, 1, 2 → primeira linha
3, 4, 5 → segunda linha
6, 7, 8 → terceira linha
O valor 0 representa o espaço vazio.
Movimentos
O espaço vazio pode trocar de posição com:
A peça acima (se existir)
A peça abaixo (se existir)
A peça à esquerda (se existir)
A peça à direita (se existir)
Verificação de Solucionabilidade
Para garantir que um estado é solucionável:

Conta-se o número de inversões (pares de números fora de ordem) ignorando o zero.
No 8-puzzle clássico (3x3), o estado é solucionável se o número de inversões for par.
Heurística: Distância de Manhattan
A função heurística 
 é a soma, para cada peça, da distância em linhas + colunas entre a posição atual e a posição final:

ç

Estrutura do A*
Usa uma fila de prioridade (heapq) para armazenar estados com base em 
:
: custo do caminho (número de movimentos)
: distância de Manhattan
Mantém:
came_from: para reconstruir o caminho de estados
g_score: melhor custo conhecido até cada estado
f_score: soma de custo + heurística
📘 Relato: Uso de IA como Tutora
Durante o desenvolvimento deste projeto, utilizamos uma ferramenta de Inteligência Artificial como apoio pedagógico, funcionando como uma espécie de “tutora virtual”.

A IA ajudou em:

Compreensão do problema

Revisão do conceito do 8-puzzle e dos requisitos da atividade.
Explicação da diferença entre algoritmos de busca (por exemplo, BFS e A*).
Justificativa da escolha do A* para eficiência e uso de heurística.
Planejamento da solução

Sugestão de representar o estado do tabuleiro com uma tupla de 9 elementos.
Explicação de como gerar vizinhos (movimentos válidos do espaço vazio).
Orientação sobre a verificação de estados solucionáveis via contagem de inversões.
Implementação do algoritmo

Auxílio na implementação da função de heurística utilizando a distância de Manhattan.
Explicação da estrutura do algoritmo A* (aberta, fechada, custos g(n) e h(n)).
Apoio na reconstrução do caminho final de estados a partir do dicionário came_from.
Interface gráfica (Tkinter)

Sugestão do uso de Tkinter para uma interface simples.
Orientação sobre como organizar os botões em uma grade 3x3.
Conexão entre os botões de controle (gerar estado aleatório, resolver, próximo passo, resetar) e as funções da lógica.
Depuração e correções

Explicação de erros de sintaxe e mensagens de exceção.
Correção de problemas de lógica na geração de vizinhos e na atualização da interface.
Sugestões de melhoria na legibilidade e organização do código.
Com isso, a IA teve um papel importante não apenas em fornecer código, mas também em explicar conceitos, apoiar o raciocínio algorítmico e ajudar a corrigir dificuldades encontradas durante o desenvolvimento.

👨‍💻 Autor
Sandro Marcos Machiniski

Disciplina: Algoritimos Avançados 
Professor(a): Glauco Vinicius Scheffel
Instituição: Universidade Católica de Santa Catarina
