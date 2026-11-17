#!/usr/bin/env python3
"""
previsao_cache.py — simulador de cache simples (LRU) para PREVER a taxa de acerto
dos acessos lw de linha.s e coluna.s. Serve para conferir os numeros do Ripes.
Uso: python3 previsao_cache.py
"""
N, BASE = 32, 0x10000000

def acessos(ordem):
    for a in range(N):
        for b in range(N):
            i, j = (a, b) if ordem == "linha" else (b, a)
            yield BASE + (i * N + j) * 4

def taxa_acerto(ordem, vias, conjuntos, palavras_bloco):
    bloco = palavras_bloco * 4
    cache = [[] for _ in range(conjuntos)]      # cada conjunto: lista LRU de tags
    acertos = total = 0
    for end in acessos(ordem):
        num_bloco = end // bloco
        idx, tag = num_bloco % conjuntos, num_bloco // conjuntos
        c = cache[idx]; total += 1
        if tag in c:
            acertos += 1; c.remove(tag)
        elif len(c) == vias:
            c.pop(0)                             # expulsa o menos usado recentemente
        c.append(tag)
    return acertos / total

CONFIGS = [  # (vias, conjuntos/linhas, palavras por bloco)
    (1, 32, 4), (4, 8, 4), (1, 32, 8), (1, 256, 4),
]
print(f"{'config':32} {'tam.':>6}  {'linha':>7}  {'coluna':>7}")
for v, s, p in CONFIGS:
    tam = v * s * p * 4
    nome = f"{v}-via, {s} linhas, {p} pal/bloco"
    print(f"{nome:32} {tam:>5}B  {taxa_acerto('linha',v,s,p):7.1%}  {taxa_acerto('coluna',v,s,p):7.1%}")
