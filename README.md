# Impacto da memória cache no desempenho de software

**Percorrendo matrizes por linha e por coluna.** Projeto prático da disciplina Arquitetura e Organização de Computadores (Sistemas de Informação, UFAL Penedo, 2026.2).

## Ideia

As duas versões somam a mesma matriz, executam as mesmas instruções e chegam ao mesmo resultado. A única diferença é a ordem dos acessos à memória:

| Percurso | Laço interno | Acessos consecutivos | Localidade espacial |
|---|---|---|---|
| Por linha | `j` (coluna) | endereços vizinhos (+4 bytes) | alta |
| Por coluna | `i` (linha) | saltos de `N × 4` bytes | quase nenhuma |

O experimento tem duas partes:

1. **Simulador (Ripes, RISC-V):** compara a **taxa de acerto da cache de dados** em ambiente controlado.
2. **Máquina real (C):** mede o **tempo de execução** para N de 64 a 4096.

## Estrutura

```
ripes/
  linha.s              # Assembly RISC-V, percurso por linha (matriz 32x32)
  coluna.s             # Assembly RISC-V, percurso por coluna
  previsao_cache.py    # simulador de cache simples para conferir o Ripes
c/
  percurso.c           # as duas versões + medição de tempo
  Makefile
experimento.py         # compila, roda todos os N e gera CSV + gráficos
resultados/            # saída do experimento
```

## Como reproduzir

### Parte 1: Ripes

1. Baixe o Ripes em https://github.com/mortbopet/Ripes/releases e abra o programa.
2. Escolha um processador **RV32IM** (o código usa `mul`).
3. Na aba **Editor**, abra `ripes/linha.s`. Na aba **Cache**, configure a cache de dados (vias, linhas, palavras por bloco).
4. Rode até o fim. O console deve imprimir `49776`. Anote o **Hit rate** da cache de dados.
5. Repita com `ripes/coluna.s` e com as outras configurações.

Para conferir: `python3 ripes/previsao_cache.py` mostra a taxa esperada em cada configuração.

### Parte 2: máquina real

Requer Linux ou WSL, com `gcc`, `make` e `python3-matplotlib`.

```bash
python3 experimento.py
```

Gera `resultados/tempos.csv`, `resultados/tempo_vs_n.png` e `resultados/razao_vs_n.png`.

## Ambiente de teste

| Item | Valor |
|---|---|
| CPU | _preencher_ |
| Cache L1d / L2 / L3 | _preencher (`lscpu` no WSL)_ |
| Sistema | Windows + WSL (Ubuntu) |
| Compilador | `gcc -O2 -fno-tree-vectorize` |

A flag `-fno-tree-vectorize` desliga a vetorização (SIMD). Assim, a diferença medida vem só da cache.

## Referências

- STALLINGS, W. *Arquitetura e Organização de Computadores*. Pearson.
- PATTERSON, D.; HENNESSY, J. *Organização e Projeto de Computadores*. Elsevier.
- TANENBAUM, A. *Organização Estruturada de Computadores*. Pearson.
- Documentação do Ripes: https://github.com/mortbopet/Ripes/wiki
