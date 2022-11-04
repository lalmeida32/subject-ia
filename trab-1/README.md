Para executar .pyde, [baixe processing](https://processing.org/download) e
instale o plugin de python.

Para executar .py, baixar python e [poetry](https://python-poetry.org/docs/),
baixe as dependências (numpy) com `poetry install` e execute com o comando
`poetry run python <arquivo>`

O arquivo checkmate.py contém a implementação do ataque a uma outra peça usando o cavalo. A função runBFS() implementa a busca em largura e a função runAStar implementa a busca com A Estrela e heurística distância de Manhattan.

O arquivo knight_tour.py contém a implementação do tour do cavalo pelo tabuleiro. A função runDFS() implementa a busca em profundidade e a função runHeuristic implementa a busca com heurística de Wandroff.
