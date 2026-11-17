#!/usr/bin/env python3
"""
experimento.py — compila, roda o experimento para varios N e gera os graficos.
Uso (de dentro da pasta do projeto):   python3 experimento.py
Saidas: resultados/tempos.csv, resultados/tempo_vs_n.png, resultados/razao_vs_n.png
"""
import csv, os, subprocess

TAMANHOS = [64, 128, 256, 512, 1024, 2048, 4096]
REPETICOES = 7

raiz = os.path.dirname(os.path.abspath(__file__))
pasta_c = os.path.join(raiz, "c")
pasta_res = os.path.join(raiz, "resultados")
os.makedirs(pasta_res, exist_ok=True)

subprocess.run(["make", "-C", pasta_c], check=True)
exe = os.path.join(pasta_c, "percurso")

linhas = []
for n in TAMANHOS:
    rep = REPETICOES if n <= 2048 else 3      # N=4096 e lento por coluna
    out = subprocess.run([exe, str(n), str(rep)], capture_output=True,
                         text=True, check=True).stdout.strip()
    n_, tl, tc, razao = out.split(",")
    kib = int(n_) ** 2 * 4 / 1024
    linhas.append([int(n_), round(kib), float(tl), float(tc), float(razao)])
    print(f"N={n_:>5} ({kib:>8.0f} KiB)  linha={float(tl):9.3f} ms  "
          f"coluna={float(tc):9.3f} ms  coluna/linha={razao}x")

with open(os.path.join(pasta_res, "tempos.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["N", "tamanho_KiB", "tempo_linha_ms", "tempo_coluna_ms", "razao"])
    w.writerows(linhas)

# ---------- graficos ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ns = [l[0] for l in linhas]
plt.figure(figsize=(7, 4.5))
plt.plot(ns, [l[2] for l in linhas], "o-", label="Por linha")
plt.plot(ns, [l[3] for l in linhas], "s-", label="Por coluna")
plt.xscale("log", base=2); plt.yscale("log")
plt.xticks(ns, [str(n) for n in ns])
plt.xlabel("N (matriz N x N de int)"); plt.ylabel("Tempo (ms, escala log)")
plt.title("Tempo para somar a matriz")
plt.grid(True, which="both", alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(pasta_res, "tempo_vs_n.png"), dpi=150)

plt.figure(figsize=(7, 4.5))
plt.bar([str(n) for n in ns], [l[4] for l in linhas])
plt.axhline(1, color="gray", linestyle="--", linewidth=1)
plt.xlabel("N"); plt.ylabel("Tempo coluna / tempo linha")
plt.title("Quantas vezes o percurso por coluna e mais lento")
plt.tight_layout(); plt.savefig(os.path.join(pasta_res, "razao_vs_n.png"), dpi=150)
print("\nGraficos salvos em resultados/")
